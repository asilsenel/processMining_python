# config/settings.py

import os

class AppSettings:
    # OpenAI API Key (Şu an kullanılmıyor ama ilerisi için hazır)
    OPENAI_MODEL: str = "gpt-4o"

    # Tarih filtresi ayarları
    DAY_LIMIT_ENABLED: bool = False # Varsayılan olarak False, UI'dan değiştirilecek
    DAY_LIMIT_DAYS: int = 30       # Varsayılan olarak 30 gün, UI'dan değiştirilecek

    # Fuzzy Match Threshold:
    MATCHING_THRESHOLD: int = 90

    # UI Dashboard için ana kök dizin (LÜTFEN KENDİ SİSTEMİNİZE GÖRE GÜNCELLEYİN!)
    # Bu dizin, her bir sürecin kendi klasörünü (örn: Holding_SPK_Sureci) içerir.
    PROCESS_MASTER_ROOT_DIR: str = r"//eczpapirus/ebidata$/RPA/Process_Mining_Surec_Dosyalari/SurecDosyalari/"

    # Raporların kaydedileceği dizin (LÜTFEN KENDİ SİSTEMİNİZE GÖRE GÜNCELLEYİN!)
    # Örnek: Kullanıcının Belgelerim klasöründe bir alt klasör
    REPORT_OUTPUT_DIR: str = os.path.join(os.path.expanduser("~"), "Documents", "ProcessMiningRaporlari")
    # Alternatif olarak, ortak bir ağ yolu olabilir:
    # REPORT_OUTPUT_DIR: str = r"\\OrtakSunucu\Raporlar\ProcessMiningGraflari"

    # Bu değişkenler main.py içinde dinamik olarak güncellenir
    PROJECT_FOLDER_PATH: str = ""
    CSV_PATH: str = ""

    @staticmethod
    def get_process_folder_names():
        """
        PROCESS_MASTER_ROOT_DIR altındaki her bir sürece ait klasör isimlerini döndürür.
        """
        process_folders = []
        if os.path.exists(AppSettings.PROCESS_MASTER_ROOT_DIR):
            for item in os.listdir(AppSettings.PROCESS_MASTER_ROOT_DIR):
                item_path = os.path.join(AppSettings.PROCESS_MASTER_ROOT_DIR, item)
                if os.path.isdir(item_path):
                    process_folders.append(item)
        else:
            print(f"Uyarı: PROCESS_MASTER_ROOT_DIR yolu bulunamadı: {AppSettings.PROCESS_MASTER_ROOT_DIR}")
            print("Lütfen config/settings.py dosyasındaki PROCESS_MASTER_ROOT_DIR yolunu kontrol edin.")
        return process_folders

    @classmethod
    def update_settings(cls, **kwargs):
        """Uygulama ayarlarını dinamik olarak günceller."""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:

                print(f"Uyarı: '{key}' adında bir ayar bulunamadı.")
