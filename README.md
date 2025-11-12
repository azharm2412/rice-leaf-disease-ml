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

| Tahap | Teknik yang Digunakan | Input | Output |
|-------|------------------------|--------|--------|
| **1. Preprocessing** | Resize (128×128), Grayscale, CLAHE, Gaussian Blur | `image: PIL` | `gray: np.ndarray` |
| **2. Segmentasi** | HSV Thresholding, Morphological Closing | `gray` | `mask: np.ndarray` |
| **3. Ekstraksi Fitur** | Mean, Std, GLCM (Contrast, Energy, Homogeneity, Correlation) | `gray` / `mask` | `feature_vector: np.ndarray` |
| **4. Klasifikasi** | Random Forest / SVM | `feature_vector` | `Label: Sehat / Penyakit` |
| **5. Aplikasi Web** | Streamlit | `File Upload (gambar)` | Hasil Prediksi & Fitur |


---



## Dataset 
* **Sumber**: 
* **Total**: 
* **Struktur**: 

## Struktur Proyek 
```css
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
```

## Setup (SEMUA ANGGOTA WAJIB)

> Pastikan sudah install **Git** dan **Python 3.10+**

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

