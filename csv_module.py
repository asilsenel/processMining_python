# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 2025
@author: asil.senel
"""
# csv_module.py

import pandas as pd
import re

def extract_selector_from_message(message):
    """
    Exception Reason içinden asıl hataya sebep olan selector'ı çeker.
    """
    if not isinstance(message, str):
        return None

    try:
        # "Search failed at selector tag:" ile "The closest matches found are:" arasını bul
        pattern = r"Search failed at selector tag:\s*\[\d+\]\s*(<.*?>)\s*The closest matches found are:"
        match = re.search(pattern, message, re.DOTALL)

        if match:
            selector = match.group(1).strip()
            return selector
        else:
            # Eğer tam pattern bulunamazsa daha basit bir alternatif
            pattern_simple = r"Search failed at selector tag:\s*\[\d+\]\s*(<.*?>)"
            match_simple = re.search(pattern_simple, message, re.DOTALL)
            if match_simple:
                selector = match_simple.group(1).strip()
                return selector

    except Exception as e:
        print(f"[extract_selector_from_message ERROR] {e}")

    return None


def extract_relevant_exceptions(csv_path):
    """
    Verilen CSV dosyasından ApplicationException ve UI selector hatalarını çıkarır.
    Output: DataFrame (Reference, Exception_Message, Selector)
    """
    print("[CSV] Relevant Exception kayıtları çıkarılıyor...")
    print(f"[CSV] CSV dosyası okunuyor... Path: {csv_path}")

    df = pd.read_csv(csv_path)

    # Sadece 'ApplicationException' içeren kayıtları seç
    df_filtered = df[df['Exception'].notna() & df['Exception'].str.contains('ApplicationException', na=False)]
    print(f"[CSV] {len(df_filtered)} adet ApplicationException bulundu.")

    # Hedef mesaj pattern'i ile filtrele
    target_phrase = "Exception message: Could not find the UI element corresponding to this selector:"
    df_filtered = df_filtered[df_filtered['Exception Reason'].str.contains(target_phrase, na=False)]
    print(f"[CSV] {len(df_filtered)} adet 'Could not find UI element' hatası bulundu.")

    # Selectorları çıkar
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

    df_extracted = pd.DataFrame(records)
    return df_extracted
