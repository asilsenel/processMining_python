# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 2025
@author: asil.senel
"""

# csv_module.py

import pandas as pd
import re
from datetime import datetime, timedelta
from config import DAY_LIMIT_ENABLED, DAY_LIMIT_DAYS

def extract_relevant_exceptions(csv_path):
    print("[CSV] Relevant Exception kayıtları çıkarılıyor...")
    df = pd.read_csv(csv_path)

    # Started sütununu güvenli bir şekilde parse et
    print("[CSV] Tarihler parse ediliyor...")
    try:
        df['Started'] = pd.to_datetime(df['Started'], format="%Y-%m-%dT%H:%M:%S.%fZ", errors='raise')
    except Exception as e:
        print(f"[CSV] Katı formatla parse başarısız oldu: {e}")
        df['Started'] = pd.to_datetime(df['Started'], errors='coerce')

    print(f"[CSV] Geçerli tarihli kayıt sayısı: {df['Started'].notna().sum()} / {len(df)}")

    # Gün filtresi uygula
    if DAY_LIMIT_ENABLED:
        print(f"[CSV] DAY_LIMIT_ENABLED aktif. Son {DAY_LIMIT_DAYS} gün içindeki kayıtlar alınacak.")
        time_limit = datetime.utcnow() - timedelta(days=DAY_LIMIT_DAYS)
        df = df[df['Started'] >= time_limit]
        print(f"[CSV] Zaman filtresinden sonra kalan kayıtlar: {len(df)} adet.")
    else:
        print("[CSV] DAY_LIMIT_ENABLED pasif. Tüm kayıtlar kullanılacak.")

    # Sadece 'ApplicationException' içeren kayıtları seç
    df_filtered = df[df['Exception'].notna() & df['Exception'].str.contains('ApplicationException', na=False)]
    print(f"[CSV] {len(df_filtered)} adet ApplicationException bulundu.")

    # Belirli mesaj içerenleri seç
    target_phrase = "Exception message: Could not find the UI element corresponding to this selector:"
    df_filtered = df_filtered[df_filtered['Exception Reason'].str.contains(target_phrase, na=False)]
    print(f"[CSV] {len(df_filtered)} adet 'Could not find UI element' hatası bulundu.")

    # Selector çıkar
    records = []
    for idx, row in df_filtered.iterrows():
        exception_message = row.get('Exception Reason', '')
        selector = extract_selector_from_message(exception_message)

        if selector:
            records.append({
                "Reference": row.get('Reference', 'Unknown'),
                "Exception_Message": exception_message,
                "Selector": selector
            })

    df_result = pd.DataFrame(records)
    print(f"[CSV] {len(df_result)} adet selector başarıyla çıkarıldı.")
    return df_result

def extract_selector_from_message(message):
    if not isinstance(message, str):
        return None

    # Yeni mantık: "Could not find the UI element corresponding to this selector:" ile "Search failed at selector tag:" arasını al
    start_tag = "Could not find the UI element corresponding to this selector:"
    end_tag = "Search failed at selector tag:"
    
    start_idx = message.find(start_tag)
    end_idx = message.find(end_tag)

    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        extracted = message[start_idx + len(start_tag):end_idx].strip()
        extracted = clean_selector_text(extracted)
        return extracted

    return None

def clean_selector_text(text):
    # [1], [2] gibi patternleri temizle
    text = re.sub(r'\[\d+\]\s*', '', text)
    return text.strip()
