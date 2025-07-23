# matching_module.py
from rapidfuzz import fuzz
import pandas as pd
from config.settings import AppSettings

def match_selectors(df_xaml: pd.DataFrame, df_csv: pd.DataFrame, threshold: int = AppSettings.MATCHING_THRESHOLD) -> pd.DataFrame:
    """
    CSV'den gelen selectorları XAML'den gelen selectorlarla fuzzy matching yapar.
    Args:
        df_xaml (pd.DataFrame): XAML'den çıkarılan aktiviteleri içeren DataFrame.
        df_csv (pd.DataFrame): CSV'den çıkarılan exception selectorlarını içeren DataFrame.
        threshold (int): 0-100 arası benzerlik eşiği.
    Returns:
        pd.DataFrame: Eşleşen selectorları içeren DataFrame.
    """
    if df_xaml.empty or df_csv.empty:
        print("⚠️ Eşleştirme için XAML veya CSV DataFrame'lerinden biri boş. Eşleşme yapılmıyor.")
        return pd.DataFrame()

    matched_records = []
    print(f"[EŞLEŞTİRME] Fuzzy eşleştirme başlatılıyor (Eşik: {threshold})...")
    
    total_csv_selectors = len(df_csv)
    for i, csv_row in df_csv.iterrows():
        csv_selector = csv_row['Selector']
        
        best_score = 0
        best_match_activity_type = None
        best_match_display_name = None
        best_match_xaml_file = None # XAML dosya bilgisini saklamak için eklendi
        best_match_xaml_selector = None # Eşleşen XAML selector'ını da saklamak için eklendi

        for _, xaml_row in df_xaml.iterrows():
            xaml_selector = xaml_row['Selector']
            score = fuzz.ratio(csv_selector, xaml_selector)
            
            if score > best_score:
                best_score = score
                best_match_activity_type = xaml_row["Activity_Type"]
                best_match_display_name = xaml_row["DisplayName"]
                best_match_xaml_file = xaml_row["XAML_File"] # XAML dosya bilgisi alındı
                best_match_xaml_selector = xaml_selector # Eşleşen XAML selector'ı kaydedildi
        
        if best_score >= threshold and best_match_activity_type is not None:
            matched_records.append({
                "Selector": csv_selector, # CSV'den gelen selector (hata veren)
                "Matched_Activity_Type": best_match_activity_type,
                "Matched_DisplayName": best_match_display_name,
                "Matched_XAML_File": best_match_xaml_file,
                "Matched_XAML_Selector": best_match_xaml_selector, # Eşleşen XAML selector'ı
                "Match_Score": best_score
            })
        
        if (i + 1) % 100 == 0 or (i + 1) == total_csv_selectors:
            print(f"[EŞLEŞTİRME] İşlenen CSV kaydı: {i+1}/{total_csv_selectors}")

    df_matched = pd.DataFrame(matched_records)
    print(f"[EŞLEŞTİRME] Toplam {len(df_matched)} eşleşen kayıt bulundu.")
    return df_matched