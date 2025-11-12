# Rice Leaf Disease Detection 

## Deskripsi Proyek 
Proyek ini bertujuan untuk mendeteksi penyakit pada daun padi menggunakan citra (gambar).  
Model Machine Learning dilatih menggunakan dataset gambar daun padi sehat dan sakit, lalu diintegrasikan ke aplikasi web berbasis **Streamlit**.  
Pengguna dapat mengunggah foto daun padi dan langsung melihat hasil prediksinya, apakah daun tersebut **sehat** atau **terkena penyakit**.

--- 

## Anggota Kelompok 
| Nama | NIM | Tugas Utama | 
|------|-----|-------------|
| Azhar Maulana | 24/533487/PA/22582 | Lorem Ipsum | 
| Dhimas Early Oceandy | 24/533508/PA/22584 | Lorem Ipsum | 
| Evan Razzan Adytaputra | 24/545257/PA/23166 | Lorem Ipsum |
| Herlina Iin Nur Soleha | 24/541333/PA/22962 | Lorem Ipsum |
| Mikail Achmad | 24/542370/PA/23026 | Lorem Ipsum | 
 
--- 

## Technical Implementation (Pipeline)
# src/preprocessing.py
def preprocess_image(pil_img, size=(128,128), use_clahe=False, blur=True) -> np.ndarray: ...

# src/segmentation.py (opsional)
def segment_leaf(rgb_or_gray: np.ndarray, method="hsv") -> np.ndarray: ...

# src/feature_extraction.py
def extract_features(gray: np.ndarray, mask: np.ndarray | None=None) -> np.ndarray:
    """Return vector: [mean, std, glcm_contrast, glcm_energy, glcm_homogeneity, glcm_correlation, ...]"""

# src/train_model.py
def train_and_save_model(X: np.ndarray, y: np.ndarray, out_path="models/rice_leaf_rf.pkl") -> None: ...

## Diagram Alur 
flowchart LR
A[Upload Gambar] --> B[Preprocessing<br/>resize, grayscale, (CLAHE, blur)]
B --> C{Perlu Segmentasi?}
C -- ya --> D[HSV/OTSU] --> E[Morfologi<br/>(opening/closing)]
C -- tidak --> E
E --> F[Ekstraksi Fitur<br/>(warna + GLCM + (LBP))]
F --> G[Model ML<br/>Random Forest / SVM]
G --> H[Prediksi: Sehat / Penyakit]

## Dataset 
* **Sumber**: 
* **Total**: 
* **Struktur**: 

## Struktur Proyek 
RICE-LEAF-DISEASE-ML/
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── rice_leaf_rf.pkl
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_segmentation.ipynb
│   ├── 03_feature_extraction.ipynb
│   ├── 04_training_model.ipynb
│   └── evaluation.ipynb
│
├── results/
│   └── metrics_report.txt
│
├── src/
│   ├── __init__.py
│   ├── feature_extraction.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── segmentation.py
│   └── train_model.py
│
├── tests/
│
├── venv/
│
├── .gitignore
├── README.md
└── requirements.txt

## Setup (SEMUA ANGGOTA WAJIB)

> Pastikan sudah install **Git** dan **Python 3.10+**.

### 1) Clone repo
```bash
git clone https://github.com/<username>/RICE-LEAF-DISEASE-ML.git
cd RICE-LEAF-DISEASE-ML
```
### 2) Buat virtual environment
```bash 
python -m venv venv
# Activate
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate
```
### 3) Install dependencies 
```bash 
pip install -r requirements.txt
```

### 4) Test enviroment
```bash 
python -c "import numpy, cv2, sklearn, skimage, joblib; print('deps OK')"
```

