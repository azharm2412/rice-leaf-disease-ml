import streamlit as st
from PIL import Image
import sys
from pathlib import Path
import time

# --- SETUP PATH (Supaya bisa import src) ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Coba import module prediksi Anda
try:
    from src.predict import predict_with_proba
except ImportError:
    # Dummy function jika file src belum siap (untuk testing UI)
    def predict_with_proba(file_bytes):
        return "brown_spot", {"brown_spot": 0.85, "healthy": 0.10, "leaf_blast": 0.05}, None, None

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="RiceGuard AI - Disease Detection",
    page_icon="🌿",
    layout="wide", # Menggunakan layout wide agar kartu di bawah terlihat bagus
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE MANAGEMENT ---
# Untuk mengatur navigasi antara Landing Page (Home) dan Halaman Analisis
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_analysis():
    st.session_state.page = 'analysis'

def go_home():
    st.session_state.page = 'home'

# --- CSS STYLING (THEME: DARK GREEN & MODERN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Reset & Base Styles */
    body { font-family: 'Inter', sans-serif; }
    
    /* Background Utama - Dark Green Gradient */
    .stApp {
        background-color: #020a05;
        background-image: radial-gradient(circle at 50% 0%, #0d3321 0%, #020a05 70%);
    }

    /* Navbar / Header Text */
    .nav-header {
        color: #4ade80; /* Light Green */
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 50px;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        max-width: 900px;
        margin: 0 auto;
    }

    .main-title {
        font-size: 64px; /* Ukuran besar seperti referensi */
        font-weight: 700;
        color: #6ee7b7; /* Cyan-Green */
        margin-bottom: 20px;
        line-height: 1.1;
    }

    .sub-title {
        font-size: 20px;
        color: #a7f3d0; /* Very light green/white */
        font-weight: 300;
        margin-bottom: 40px;
        line-height: 1.6;
    }

    /* Custom Button Style untuk meniru tombol biru di referensi */
    div.stButton > button {
        background-color: #10b981; /* Emerald Green */
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 12px 32px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
    }
    div.stButton > button:hover {
        background-color: #059669;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
    }

    /* Cards Section */
    .card-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-top: 60px;
    }
    
    /* Individual Card styling mimicking the reference */
    .feature-card {
        background: rgba(6, 78, 59, 0.2); /* Transparan dark green */
        border: 1px solid #34d399; /* Border hijau terang tipis */
        border-radius: 12px;
        padding: 30px 20px;
        text-align: center;
        color: white;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(6, 78, 59, 0.4);
    }
    
    .card-icon {
        font-size: 40px;
        margin-bottom: 15px;
        color: #6ee7b7;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #ecfdf5;
        margin-bottom: 10px;
    }
    
    .card-desc {
        font-size: 14px;
        color: #d1fae5;
        line-height: 1.5;
    }

    /* Styling khusus untuk halaman upload (Analysis Page) */
    .upload-box {
        background: #064e3b;
        padding: 30px;
        border-radius: 15px;
        border: 2px dashed #34d399;
        text-align: center;
    }
    .result-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #10b981;
        padding: 20px;
        margin-top: 20px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HALAMAN 1: LANDING PAGE (Mirip Screenshot) ---
if st.session_state.page == 'home':
    # Header Icon
    st.markdown('<div class="nav-header">🌿 Plant Disease Diagnosis System</div>', unsafe_allow_html=True)
    
    # Hero Section (Judul & Tombol)
    st.markdown("""
        <div class="hero-container">
            <div class="main-title">Rice Leaf Disease<br>Analysis System</div>
            <div class="sub-title">
                An advanced AI platform to assist farmers and agronomists in detecting and analyzing 
                rice plant conditions through leaf images with high accuracy.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tombol Start (Menggunakan st.columns biar di tengah)
    col_spacer1, col_btn, col_spacer2 = st.columns([1, 0.5, 1])
    with col_btn:
        st.button("Start Analysis", on_click=go_to_analysis, use_container_width=True)

    # Cards Section (4 Kolom)
    st.write("") # Spacer
    st.write("") 
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🧠</div>
                <div class="card-title">Advanced AI</div>
                <div class="card-desc">Leading Deep Learning technology (CNN) for precise leaf pattern analysis.</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🛡️</div>
                <div class="card-title">Safe & Fast</div>
                <div class="card-desc">Process images locally or securely in the cloud with rapid inference times.</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">🌾</div>
                <div class="card-title">For Agronomists</div>
                <div class="card-desc">The platform is specifically tuned for rice varieties and common diseases.</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="card-icon">📊</div>
                <div class="card-title">Detailed Report</div>
                <div class="card-desc">Get comprehensive confidence scores and disease classification history.</div>
            </div>
        """, unsafe_allow_html=True)


# --- HALAMAN 2: ANALYSIS PAGE (Fungsionalitas Utama) ---
elif st.session_state.page == 'analysis':
    # Tombol Back (Kecil di pojok kiri)
    if st.button("← Back to Home"):
        go_home()
        st.rerun()

    st.markdown("<h2 style='text-align: center; color: #6ee7b7;'>Upload Leaf Image</h2>", unsafe_allow_html=True)

    # Layout: Kiri (Upload), Kanan (Hasil)
    col_upload, col_result = st.columns([1, 1])

    uploaded_file = None
    
    with col_upload:
        st.markdown("### Source Image")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Tombol Analyze
            analyze_clicked = st.button("🔍 Run Diagnosis", use_container_width=True)

    with col_result:
        st.markdown("### Diagnosis Result")
        
        if uploaded_file and analyze_clicked:
            file_bytes = uploaded_file.getvalue()
            
            with st.spinner("Analyzing leaf patterns..."):
                # Simulasi sedikit delay biar kerasa 'mikir'
                time.sleep(1)
                
                # --- PANGGIL FUNGSI PREDIC DARI SRC ---
                label_raw, proba_dict, _, _ = predict_with_proba(file_bytes)
            
            # Formatting Label
            label_clean = label_raw.replace("_", " ").title()
            confidence = proba_dict[label_raw] * 100
            
            # Menentukan warna berdasarkan hasil
            if label_raw == "healthy":
                res_color = "#4ade80" # Hijau terang
                emoji = "✅"
            else:
                res_color = "#fb7185" # Merah rose
                emoji = "⚠️"

            # Tampilan Hasil (Card Style)
            st.markdown(f"""
                <div class="result-box">
                    <div style="font-size: 14px; color: #a7f3d0;">PREDICTED CONDITION</div>
                    <div style="font-size: 36px; font-weight: bold; color: {res_color};">
                        {emoji} {label_clean}
                    </div>
                    <div style="font-size: 16px; color: white; margin-top: 10px;">
                        Confidence: <b>{confidence:.2f}%</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Breakdown Progress Bars
            st.markdown("<br><b>Detailed Probabilities:</b>", unsafe_allow_html=True)
            
            # Sort probabilitas
            sorted_probs = dict(sorted(proba_dict.items(), key=lambda item: item[1], reverse=True))
            
            for disease, prob in sorted_probs.items():
                if prob > 0.01: # Tampilkan hanya yang > 1%
                    d_name = disease.replace("_", " ").title()
                    st.write(f"{d_name}")
                    st.progress(prob)
        
        elif not uploaded_file:
            st.info("Waiting for image upload...")
            st.markdown("""
                <div style="color: #6b7280; font-size: 14px; margin-top: 20px;">
                    Supported formats: JPG, PNG<br>
                    Ensure the leaf is clearly visible and well-lit.
                </div>
            """, unsafe_allow_html=True)