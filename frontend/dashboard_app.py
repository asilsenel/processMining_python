# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:55:06 2025

@author: asil.senel
"""
# dashboard_app.py

import streamlit as st
from PIL import Image
import requests

# FastAPI sunucu URL'in
API_URL = "http://127.0.0.1:8000/start-analysis"

# Sayfa ayarları
st.set_page_config(
    page_title="Process Mining Dashboard",
    page_icon="🧠",
    layout="centered",
)

# Logo (PNG) Ekle
logo_path = "beyin.png"  # Aynı klasöre beyin.png'yi koy
image = Image.open(logo_path)
st.image(image, width=100)

# Başlık
st.title("Process Mining Dashboard")

# Süreç Seçimi
process_options = ["EB RPA Paket Yükleme Süreci"]  # Şimdilik manuel liste
selected_process = st.selectbox("Süreç Seçin:", process_options)

# Gün limiti
day_limit_days = st.number_input("İşlenecek gün sayısı:", min_value=1, max_value=365, value=30, step=1)
day_limit_enabled = st.checkbox("Gün kısıtı aktif olsun mu?", value=True)

# AI Powered Switch
use_ai = st.checkbox("AI Powered", value=False)

# Buton
if st.button("Analizi Başlat"):
    # Backend'e gönderilecek payload
    payload = {
        "process_name": selected_process,
        "day_limit_enabled": day_limit_enabled,
        "day_limit_days": int(day_limit_days),
        "use_ai": use_ai
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            st.success(f"✅ Analiz başlatıldı: {selected_process}")
        else:
            st.error(f"❌ Hata oluştu: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Sunucuya bağlanılamadı: {e}")
