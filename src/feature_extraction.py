# src/feature_extraction.py

from __future__ import annotations
import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops

def load_gray_and_mask_from_segmented(seg_bgr: np.ndarray):
    if seg_bgr is None:
        raise ValueError("Gambar segmented kosong / None")

    gray = cv2.cvtColor(seg_bgr, cv2.COLOR_BGR2GRAY)
    mask = (gray > 0).astype("uint8")
    return gray, mask


def extract_features(
    gray: np.ndarray,
    mask: np.ndarray | None = None,
    distances=[1, 3, 5],
    angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
    levels: int = 256,
):

    # fokus area daun
    if mask is not None:
        roi = gray.copy()
        roi[mask == 0] = 0
        values = gray[mask > 0]
        if values.size == 0:
            values = gray.flatten()
    else:
        roi = gray
        values = gray.flatten()

    # normalisasi ke 0–255 untuk GLCM
    roi_norm = cv2.normalize(roi, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")

    # GLCM
    glcm = graycomatrix(
        roi_norm,
        distances=distances,
        angles=angles,
        levels=levels,
        symmetric=True,
        normed=True,
    )

    feats = {}

    glcm_props = ["contrast", "dissimilarity", "homogeneity",
                  "energy", "ASM", "correlation"]

    for prop in glcm_props:
        vals = graycoprops(glcm, prop)
        feats[f"{prop}_mean"] = float(vals.mean())
        feats[f"{prop}_std"]  = float(vals.std())

    # entropy + cluster features
    glcm_mean = glcm.mean(axis=(2, 3))
    p = glcm_mean.astype(np.float64)
    p /= p.sum() + 1e-12

    p_nonzero = p[p > 0]
    entropy = -np.sum(p_nonzero * np.log2(p_nonzero))
    feats["entropy"] = float(entropy)

    i_idx, j_idx = np.indices((levels, levels))
    mu_x = np.sum(i_idx * p)
    mu_y = np.sum(j_idx * p)

    s = (i_idx + j_idx - mu_x - mu_y)
    feats["cluster_shade"]      = float(np.sum((s ** 3) * p))
    feats["cluster_prominence"] = float(np.sum((s ** 4) * p))

    # statistik intensitas
    values = values.astype(np.float64)
    feats["intensity_mean"] = float(values.mean())
    feats["intensity_std"]  = float(values.std())
    feats["intensity_var"]  = float(values.var())

    return feats
