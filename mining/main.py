# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 15:57:59 2025

@author: asil.senel
"""

# main.py


from config import PROJECT_FOLDER_PATH, CSV_PATH, MATCHING_THRESHOLD
from xaml_module import extract_xaml_activities
from csv_module import extract_relevant_exceptions
from matching_module import match_selectors
from visualization_module import visualize_matched_selectors

def main():
    print("🏁 MAIN çalışıyor...")

    # XAML aktivitelerini çek
    df_xaml = extract_xaml_activities(folder_path=PROJECT_FOLDER_PATH)
    print(f"✅ XAML DF oluşturuldu: {len(df_xaml)} kayıt.")

    # CSV'den hataları çek
    df_csv = extract_relevant_exceptions(csv_path=CSV_PATH)
    print(f"✅ CSV DF oluşturuldu: {len(df_csv)} kayıt.")

    # (Şimdilik sadece DF'leri return ediyoruz, ileride eşleşme işlemi buraya eklenecek.)
    #return df_xaml, df_csv
    
    df_matched = match_selectors(df_xaml, df_csv, threshold=MATCHING_THRESHOLD)
    visualize_matched_selectors(df_matched)
    return df_matched, df_xaml, df_csv

    

if __name__ == "__main__":
    df_matched, df_xaml, df_csv = main()

