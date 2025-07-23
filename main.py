# main.py
import os
import pandas as pd

from config.settings import AppSettings
from xaml_module import extract_xaml_activities
from csv_module import extract_relevant_exceptions
from matching_module import match_selectors
from visualization_module import visualize_matched_selectors

def _perform_analysis(process_name: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Analiz adımlarını yürüten yardımcı fonksiyon."""
    print(f"🏁 '{process_name}' için analiz adımları başlatılıyor...")

    # XAML aktivitelerini oku
    df_xaml = extract_xaml_activities(folder_path=AppSettings.PROJECT_FOLDER_PATH)
    print(f"✅ XAML DataFrame oluşturuldu: {len(df_xaml)} kayıt.")

    # CSV Exception kayıtlarını oku
    df_csv = extract_relevant_exceptions(csv_path=AppSettings.CSV_PATH)
    print(f"✅ CSV DataFrame oluşturuldu: {len(df_csv)} kayıt.")

    # Eşleştirme yap
    df_matched = match_selectors(df_xaml, df_csv, threshold=AppSettings.MATCHING_THRESHOLD)
    print(f"✅ Eşleşen kayıtlar: {len(df_matched)}")

    return df_matched, df_xaml, df_csv

def main():
    """Uygulamayı doğrudan çalıştıran ana fonksiyon (yerel test için)."""
    print("🚀 Uygulama başlatılıyor...")
    # Bu fonksiyon UI'dan çağrıldığında kullanılmaz, sadece yerel test/CLI çalıştırması içindir.
    print("UI Dashboard'u kullanmak için 'python app.py' komutunu çalıştırın.")

def run_analysis(process_name: str, day_limit_enabled: bool, day_limit_days: int, use_ai: bool, project_root: str, queue_root: str, output_file_path: str) -> pd.DataFrame:
    """
    Backend'den çağrılmak üzere tasarlanmış, dinamik konfigürasyonlu analiz fonksiyonu.
    Args:
        process_name (str): Analiz edilecek sürecin adı.
        day_limit_enabled (bool): Gün kısıtlamasının aktif olup olmadığı.
        day_limit_days (int): Gün kısıtlaması kaç gün olduğu.
        use_ai (bool): AI desteğinin kullanılıp kullanılmayacağı (şu an için opsiyonel).
        project_root (str): Analiz edilecek sürecin kök dizini (örn: C:/.../SurecDosyalari/Holding_SPK_Sureci)
                             Bu dizinin içinde UiPath proje klasörü (örn: Holding_SPK_1_0_7) ve CSV dosyası beklenir.
        queue_root (str): Queue item CSV dosyasının bulunduğu kök dizin (project_root ile aynı olabilir)
        output_file_path (str): HTML raporunun kaydedileceği tam dosya yolu.
    Returns:
        pd.DataFrame: Eşleşen selectorları içeren DataFrame.
    """
    print(f"\n🚀 '{process_name}' için analiz başlatılıyor (backend çağrısı)...")
    print(f"  Rapor Çıktı Yolu: {output_file_path}")

    # Runtime ayarlarını güncelle
    found_project_folder = None
    # project_root'un kendisi process_name'i içeren klasör olduğunu varsayıyoruz,
    # yani onun altındaki UiPath proje klasörünü arıyoruz.
    for item in os.listdir(project_root):
        item_path = os.path.join(project_root, item)
        if os.path.isdir(item_path) and not item.startswith('.') and not item.startswith('__'):
            # UiPath projesinin içinde .xaml dosyalarını içeren klasörü bulmaya çalışıyoruz.
            # Örneğin, "Holding_SPK_1_0_7" klasörünü bulacak.
            if any(f.endswith(".xaml") for f in os.listdir(item_path)):
                found_project_folder = item_path
                break
    
    found_csv_file = None
    for item in os.listdir(queue_root):
        item_path = os.path.join(queue_root, item)
        if os.path.isfile(item_path) and item.lower().endswith('.csv'):
            found_csv_file = item_path
            break

    if not found_project_folder:
        raise FileNotFoundError(f"'{project_root}' dizininde UiPath proje klasörü (içinde .xaml dosyaları olan bir alt klasör) bulunamadı.")
    if not found_csv_file:
        raise FileNotFoundError(f"'{queue_root}' dizininde CSV dosyası bulunamadı.")

    AppSettings.update_settings(
        PROJECT_FOLDER_PATH=found_project_folder,
        CSV_PATH=found_csv_file,
        DAY_LIMIT_ENABLED=day_limit_enabled,
        DAY_LIMIT_DAYS=day_limit_days
    )

    print(f"⚙️ Güncel Ayarlar: PROJECT_FOLDER_PATH='{AppSettings.PROJECT_FOLDER_PATH}', CSV_PATH='{AppSettings.CSV_PATH}'")
    print("🤖 AI desteği:", "Aktif" if use_ai else "Kapalı")

    df_matched, df_xaml, df_csv = _perform_analysis(process_name=process_name)

    # Görselleştirme yap
    # visualize_matched_selectors fonksiyonuna output_file_path'i iletiyoruz
    visualize_matched_selectors(df_matched, process_name=process_name, output_file_path=output_file_path)
    
    print(f"✅ '{process_name}' için analiz tamamlandı ve görselleştirme yapıldı.")
    return df_matched

if __name__ == "__main__":
    main()