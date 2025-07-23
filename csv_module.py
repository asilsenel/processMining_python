# csv_module.py
import pandas as pd
import re
from datetime import datetime, timedelta
from config.settings import AppSettings # Yeni yapılandırma dosyamızdan import

def clean_selector_text(text: str) -> str | None:
    """Selector metninden gereksiz kısımları temizler."""
    if not isinstance(text, str):
        return None
    # [1], [2] gibi patternleri temizle
    text = re.sub(r'\[\d+\]\s*', '', text)
    return text.strip()

def extract_selector_from_message_vectorized(message: str) -> str | None:
    """
    Hata mesajından UI selector'ü çıkarmak için vectorized versiyon.
    Pandas Series üzerinde uygulanabilir.
    """
    if not isinstance(message, str):
        return None

    start_tag = "Could not find the UI element corresponding to this selector:"
    end_tag = "Search failed at selector tag:"

    start_idx = message.find(start_tag)
    end_idx = message.find(end_tag)

    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        extracted = message[start_idx + len(start_tag):end_idx].strip()
        return clean_selector_text(extracted)
    return None

def extract_relevant_exceptions(csv_path: str) -> pd.DataFrame:
    """
    Verilen CSV dosyasından ilgili istisna kayıtlarını çıkarır.
    """
    print("[CSV] İlgili Exception kayıtları çıkarılıyor...")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"[CSV Hata] '{csv_path}' dosyası bulunamadı. Boş DataFrame döndürülüyor.")
        return pd.DataFrame()
    except Exception as e:
        print(f"[CSV Hata] CSV okuma hatası: {e}. Boş DataFrame döndürülüyor.")
        return pd.DataFrame()

    # 'Started' sütununu güvenli bir şekilde parse et
    print("[CSV] Tarihler parse ediliyor...")
    initial_rows = len(df)
    # errors='coerce' ile geçersiz tarihleri NaT (Not a Time) yapar
    # utc=True ile timezone farklarını ortadan kaldırmak için önerilir
    df['Started'] = pd.to_datetime(df['Started'], errors='coerce', utc=True) 
    valid_dates_count = df['Started'].notna().sum()
    print(f"[CSV] Geçerli tarihli kayıt sayısı: {valid_dates_count} / {initial_rows}")

    if valid_dates_count == 0 and initial_rows > 0:
        print("[CSV Uyarı] Hiçbir tarih parse edilemedi. Gün filtrelemesi doğru çalışmayabilir.")

    # Gün filtresi uygula
    if AppSettings.DAY_LIMIT_ENABLED:
        print(f"[CSV] DAY_LIMIT_ENABLED aktif. Son {AppSettings.DAY_LIMIT_DAYS} gün içindeki kayıtlar alınacak.")
        # UTC now kullanarak timezone sorunlarını önle, .replace(tzinfo=None) ile karşılaştırma için naif datetime'a çevir
        time_limit = datetime.utcnow().replace(tzinfo=None) - timedelta(days=AppSettings.DAY_LIMIT_DAYS)
        # Parse edilen 'Started' sütununu da karşılaştırma için timezone'dan arındır
        df = df[df['Started'].dt.tz_localize(None) >= time_limit].copy()
        print(f"[CSV] Zaman filtresinden sonra kalan kayıtlar: {len(df)} adet.")
    else:
        print("[CSV] DAY_LIMIT_ENABLED pasif. Tüm kayıtlar kullanılacak.")

    # Sadece 'ApplicationException' içeren ve belirli mesajı içeren kayıtları seç
    # .copy() kullanımı SettingWithCopyWarning'i önler
    df_filtered = df[
        df['Exception'].notna() &
        df['Exception'].str.contains('ApplicationException', na=False) &
        df['Exception Reason'].notna() &
        df['Exception Reason'].str.contains("Could not find the UI element corresponding to this selector:", na=False)
    ].copy() 

    print(f"[CSV] {len(df_filtered)} adet 'Could not find UI element' hatası bulundu.")

    # Selector çıkar: vectorized fonksiyonu doğrudan Series üzerinde uygula
    df_filtered['Selector'] = df_filtered['Exception Reason'].apply(extract_selector_from_message_vectorized)

    # Başarıyla selector çıkarılanları al
    df_result = df_filtered[df_filtered['Selector'].notna()].copy()
    print(f"[CSV] {len(df_result)} adet selector başarıyla çıkarıldı.")

    # Sadece gerekli sütunları döndür
    return df_result[['Reference', 'Exception Reason', 'Selector']]