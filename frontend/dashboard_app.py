# dashboard_app.py

import streamlit as st
from PIL import Image
import requests

# FastAPI sunucu URL'i
API_URL = "http://127.0.0.1:8000"

# Sayfa ayarları
st.set_page_config(
    page_title="Process Mining Dashboard",
    page_icon="🧠",
    layout="centered",
)

# Logo Ekle
logo_path = "beyin.png"  # Aynı klasörde beyin.png olmalı
image = Image.open(logo_path)
st.image(image, width=100)

# Başlık
st.title("Process Mining Dashboard")

# Süreç Seçimi
process_options = [
    "EB RPA Paket Yükleme Süreci",
    "Örnek Süreç 2",
    "Örnek Süreç 3"
]  # Şimdilik sabit

selected_process = st.selectbox("Süreç Seçin:", process_options)

# Orchestrator Bağlantı Butonu
if st.button("Orchestrator ile Bağlan"):
    st.info("🔌 Orchestrator bağlantısı henüz aktif değil.")

# Gün limiti
day_limit_days = st.number_input("İşlenecek gün sayısı:", min_value=1, max_value=365, value=30, step=1)
day_limit_enabled = st.checkbox("Gün kısıtı aktif olsun mu?", value=True)

# AI Powered Switch
use_ai = st.checkbox("AI Powered", value=False)

# Süreç Pathlerini Bulma
if selected_process:
    if st.button("Pathleri Getir"):
        try:
            payload = {"process_name": selected_process}
            response = requests.post(f"{API_URL}/find-paths", json=payload)

            if response.status_code == 200:
                data = response.json()

                # Gelen pathleri göster
                st.success("📂 Proje ve CSV Pathleri bulundu!")
                st.write(f"**Project Folder Path:** {data['project_folder_path']}")
                st.write(f"**CSV File Path:** {data['csv_file_path']}")
                st.write(f"**Project Match Score:** {data['project_score']}")
                st.write(f"**Queue Match Score:** {data['queue_score']}")

            else:
                st.error(f"❌ Hata oluştu: {response.status_code}")

        except Exception as e:
            st.error(f"❌ Sunucuya bağlanılamadı: {e}")

# Analizi Başlat Butonu
if st.button("Analizi Başlat"):
    try:
        payload = {
            "process_name": selected_process,
            "day_limit_enabled": day_limit_enabled,
            "day_limit_days": int(day_limit_days),
            "use_ai": use_ai
        }
        response = requests.post(f"{API_URL}/analyze", json=payload)

        if response.status_code == 200:
            st.success(f"✅ Analiz başlatıldı: {selected_process}")
        else:
            st.error(f"❌ Hata oluştu: {response.status_code}")

    except Exception as e:
        st.error(f"❌ Sunucuya bağlanılamadı: {e}")
