# src/predict.py
# fitur 

from pathlib import Path
import numpy as np
import cv2
import joblib

from .feature_extraction import extract_features

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "rice_leaf_xgb.pkl"

CLASS_NAMES = [
    'bacterial_leaf_blight', 
    'brown_spot', 
    'healthy', 
    'leaf_blast',
    'leaf_scald', 
    'narrow_brown_spot'
]

FEATURE_COLS = [
    'contrast_mean',
    'contrast_std',
    'dissimilarity_mean',
    'dissimilarity_std',
    'homogeneity_mean',
    'homogeneity_std',
    'energy_mean',
    'energy_std',
    'ASM_mean',
    'ASM_std',
    'correlation_mean',
    'correlation_std',
    'entropy',
    'cluster_shade',
    'cluster_prominence',
    'intensity_mean',
    'intensity_std',
    'intensity_var'
]

# load model 
model = joblib.load(MODEL_PATH)
# print("MODEL CLASS ORDER:", model.classes_)

# fungsi segmentasi

def segment_leaf(img_bgr: np.ndarray):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # range HSV dari notebook
    lower = np.array([15, 40, 20])
    upper = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    segmented = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_cleaned)
    return segmented, mask_cleaned


# fungsi pipeline dari gambar → fitur

def prepare_features_from_image_bytes(file_bytes: bytes):

    # bytes → BGR image
    file_array = np.frombuffer(file_bytes, np.uint8)
    img_bgr = cv2.imdecode(file_array, cv2.IMREAD_COLOR)

    if img_bgr is None:
        raise ValueError("Gambar tidak bisa dibaca")

    img_bgr = cv2.resize(img_bgr, (128, 128))

    # segmentasi
    segmented, mask = segment_leaf(img_bgr)

    # gray + mask biner
    gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
    mask_bin = (mask > 0).astype("uint8")

    # ekstraksi fitur
    feats_dict = extract_features(gray, mask_bin)

    # susun vektor fitur 
    x = np.array([[feats_dict[col] for col in FEATURE_COLS]], dtype=np.float32)

    return x, img_bgr, segmented


def predict_image(file_bytes: bytes):
    x, img_bgr, segmented = prepare_features_from_image_bytes(file_bytes)
    y_pred_idx = int(model.predict(x)[0])  # model XGBoost mengeluarkan index kelas
    label = CLASS_NAMES[y_pred_idx]
    return label, img_bgr, segmented

def predict_with_proba(file_bytes: bytes):
    x, img_bgr, segmented = prepare_features_from_image_bytes(file_bytes)

    # probabilitas per kelas dari XGBoost
    proba = model.predict_proba(x)[0]  # shape: (n_classes,)

    # index kelas dengan prob terbesar
    idx_max = int(np.argmax(proba))
    label = CLASS_NAMES[idx_max]

    # bikin dict: {kelas: prob_float}
    proba_dict = {
        CLASS_NAMES[i]: float(proba[i])
        for i in range(len(CLASS_NAMES))
    }

    return label, proba_dict, img_bgr, segmented
