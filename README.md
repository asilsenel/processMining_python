UiPath Selector Hata Analizi ve Görselleştirme Aracı
Bu Python projesi, UiPath RPA süreçlerinizde meydana gelen "UI Element Bulunamadı" tipi selector hatalarını analiz etmek ve görselleştirmek için geliştirilmiştir. Orchestrator'dan dışa aktarılan Queue Item detayları (CSV formatında) ile UiPath proje klasörlerindeki XAML dosyalarını karşılaştırarak en çok hata veren aktiviteleri tespit eder ve interaktif bir rapor halinde sunar.

🚀 Özellikler
XAML Dosya Okuma: Belirtilen UiPath proje klasöründeki tüm XAML workflow dosyalarını tarar.

Aktivite ve Selector Çıkarımı: XAML dosyalarından aktivite DisplayName'lerini ve ilgili UI selector'larını çıkarır.

CSV Hata Ayıklama: Orchestrator'dan alınan Queue Item CSV dosyasındaki "Could not find the UI element corresponding to this selector" hatalarını ayıklar ve hata veren selector'ları parse eder.

Fuzzy Eşleştirme: CSV'den gelen hatalı selector'ları XAML'den çıkarılan selector'larla fuzzy logic kullanarak eşleştirir (RapidFuzz kütüphanesi ile). Bu sayede küçük farklılıklar olsa bile doğru eşleşmeler yapılabilir.

Zaman Filtreleme: Belirli bir gün aralığındaki (örn: son 30 gün) hataları analiz etme seçeneği sunar.

Görselleştirme: Eşleşen hatalar içinde en sık tekrar eden aktivite DisplayName'lerini bir bar grafik ile görselleştirir.

Detaylı Hover Bilgisi: Grafik üzerindeki bir barın üzerine gelindiğinde (hover), ilgili aktivitenin tüm eşleşen selector bilgilerini gösterir, bu da aynı DisplayName'e sahip farklı selector'ları ayırt etmenizi sağlar.

Web Dashboard: Kullanıcı dostu bir Flask web arayüzü üzerinden süreç seçimi, zaman filtresi ayarı ve analizi başlatma imkanı sunar.

🛠️ Kurulum
Bu projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Python Ortamı
Python 3.8+ kurulu olduğundan emin olun. Sanal ortam kullanmanız önerilir:

Bash

python -m venv venv
# Windows için
.\venv\Scripts\activate
# macOS/Linux için
source venv/bin/activate
2. Bağımlılıklar
Proje bağımlılıklarını yükleyin:

Bash

pip install pandas rapidfuzz plotly Flask
3. Konfigürasyon Ayarları
config/settings.py dosyasını kendi ortamınıza göre düzenlemeniz gerekmektedir:

Python

# config/settings.py

class AppSettings:
    # ... diğer ayarlar ...

    # UI Dashboard için ana kök dizin
    # BU YOLU KENDİ SİSTEMİNİZDEKİ RPA SÜREÇLERİNİZİN KLASÖRÜNE GÖRE GÜNCELLEYİN!
    # Örn: C:/RPA_Projelerim/SurecDosyalari/
    PROCESS_MASTER_ROOT_DIR: str = r"//eczpapirus/ebidata$/RPA/Process_Mining_Surec_Dosyalari/SurecDosyalari/"

    # Raporların kaydedileceği dizin
    # BU YOLU KENDİ SİSTEMİNİZDE RAPORLARIN KAYDEDİLECEĞİ DİZİNE GÖRE GÜNCELLEYİN!
    # Örn: C:/Kullanicilar/Adiniz/Belgelerim/ProcessMiningRaporlari/
    REPORT_OUTPUT_DIR: str = os.path.join(os.path.expanduser("~"), "Documents", "ProcessMiningRaporlari")

    # ... diğer ayarlar ...
PROCESS_MASTER_ROOT_DIR: UiPath süreç klasörlerinizin bulunduğu ana dizini belirtin. Her bir süreç (örn: Holding_SPK_Sureci), bu ana dizin altında bir klasör olmalıdır.

REPORT_OUTPUT_DIR: Oluşturulan HTML raporlarının kaydedileceği dizini belirtin.

📂 Proje Yapısı
.
├── config/
│   └── settings.py         # Uygulama genel ayarları ve yapılandırma
├── csv_module.py           # CSV dosyasından hata loglarını işleme ve selector ayıklama
├── matching_module.py      # XAML ve CSV selector'larını eşleştirme (fuzzy logic)
├── xaml_module.py          # XAML dosyalarını okuma ve aktivite/selector çıkarma
├── visualization_module.py # Analiz sonuçlarını görselleştirme (Plotly)
├── main.py                 # Core analiz mantığını çalıştıran modül
├── app.py                  # Flask web arayüzü uygulaması
└── templates/
    └── index.html          # Web dashboard'unun HTML şablonu
🏃‍♀️ Kullanım
Flask Uygulamasını Başlatın:
Projenizin ana dizininde bir terminal açın ve aşağıdaki komutu çalıştırın:

Bash

python app.py
Bu komut, Flask geliştirme sunucusunu başlatacak ve varsayılan tarayıcınızda otomatik olarak dashboard'u açacaktır (http://127.0.0.1:5000).

Dashboard Kullanımı:

Web arayüzünden analiz etmek istediğiniz süreci seçin. Süreç isimleri, PROCESS_MASTER_ROOT_DIR altında bulunan klasör isimlerinden otomatik olarak listelenir.

Gün Limiti Aktif kutucuğunu işaretleyerek belirli bir gün aralığındaki hataları analiz edebilirsiniz.

Gün Sayısı alanına kaç günlük veriyi analiz etmek istediğinizi girin (Gün Limiti Aktif olduğunda kullanılır).

Analizi Başlat butonuna tıklayın.

Rapor Çıktısı:
Analiz tamamlandığında, hata analizi grafiğini içeren bir HTML dosyası (hata_analizi_grafigi_[süreç_adı]_selector_detayli.html) REPORT_OUTPUT_DIR'da oluşturulacak ve otomatik olarak tarayıcınızda yeni bir sekmede açılacaktır. Bu interaktif grafikte çubukların üzerine geldiğinizde (hover), ilgili aktivitenin hata sayısı ve eşleşen tüm selector bilgileri görünecektir.

Uygulamayı Kapatma:
Dashboard sayfasının sağ üst köşesindeki Uygulamayı Kapat butonuna tıklayarak Flask sunucusunu güvenli bir şekilde kapatabilirsiniz.
