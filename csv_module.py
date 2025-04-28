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

    # Tarih filtresi uygulanacak mı?
    if DAY_LIMIT_ENABLED:
        print(f"[CSV] DAY_LIMIT_ENABLED aktif. Son {DAY_LIMIT_DAYS} gün içindeki kayıtlar alınacak.")
        df['Started'] = pd.to_datetime(df['Started'], errors='coerce')
        time_limit = datetime.utcnow() - timedelta(days=DAY_LIMIT_DAYS)
        df = df[df['Started'] >= time_limit]
        print(f"[CSV] Zaman filtresinden sonra kalan kayıtlar: {len(df)} adet.")
    else:
        print("[CSV] DAY_LIMIT_ENABLED pasif. Tüm kayıtlar kullanılacak.")

    # Sadece 'ApplicationException' içeren kayıtları seçelim
    df_filtered = df[df['Exception'].notna() & df['Exception'].str.contains('ApplicationException', na=False)]
    print(f"[CSV] {len(df_filtered)} adet ApplicationException bulundu.")

    # Belirli hata mesajı pattern'i ile süzelim
    target_phrase = "Exception message: Could not find the UI element corresponding to this selector:"
    df_filtered = df_filtered[df_filtered['Exception Reason'].str.contains(target_phrase, na=False)]
    print(f"[CSV] {len(df_filtered)} adet 'Could not find UI element' hatası bulundu.")

    # Selectorları çıkaralım
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

    print(f"[CSV] {len(records)} adet selector başarıyla çıkarıldı.")
    df_result = pd.DataFrame(records)
    return df_result

def extract_selector_from_message(message):
    """
    Exception Reason içinden selector'ı ayıkla.
    Yeni mantık: 
    'Could not find the UI element corresponding to this selector:' ile
    'Search failed at selector tag:' arasında kalan kısım alınacak.
    """
    if not isinstance(message, str):
        return None

    try:
        start_text = "Could not find the UI element corresponding to this selector:"
        end_text = "Search failed at selector tag:"

        start_idx = message.index(start_text) + len(start_text)
        end_idx = message.index(end_text)

        selector_block = message[start_idx:end_idx].strip()

        # [1], [2] gibi baştaki numaraları sil
        selector_lines = selector_block.splitlines()
        cleaned_selectors = []
        for line in selector_lines:
            line = line.strip()
            if line.startswith('['):
                # "]" işaretinden sonrasını al
                closing_idx = line.find(']')
                if closing_idx != -1:
                    line = line[closing_idx+1:].strip()
            if line:  # boş olmayan satırları al
                cleaned_selectors.append(line)

        final_selector = "\n".join(cleaned_selectors)
        return final_selector if final_selector else None

    except (ValueError, IndexError):
        return None
