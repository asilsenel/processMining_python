# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from config.settings import AppSettings # AppSettings'i import ediyoruz
from main import run_analysis # main.py'deki run_analysis fonksiyonunu import ediyoruz
import webbrowser # Tarayıcı açmak için
import time # Gecikme için

app = Flask(__name__)

# Flask'ı kapatmak için rota
@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# Ana sayfa (dashboard)
@app.route('/')
def index():
    process_names = AppSettings.get_process_folder_names()
    # Varsayılan gün limiti ayarları (settings.py'den çekiliyor)
    default_day_limit_enabled = AppSettings.DAY_LIMIT_ENABLED
    default_day_limit_days = AppSettings.DAY_LIMIT_DAYS
    return render_template('index.html',
                           process_names=process_names,
                           default_day_limit_enabled=default_day_limit_enabled,
                           default_day_limit_days=default_day_limit_days)

# Analiz rotası
@app.route('/analyze', methods=['POST'])
def analyze():
    selected_process_folder_name = request.form.get('process_name')
    day_limit_enabled = request.form.get('day_limit_enabled') == 'true'
    day_limit_days_str = request.form.get('day_limit_days')
    day_limit_days = int(day_limit_days_str) if day_limit_days_str else AppSettings.DAY_LIMIT_DAYS

    # project_root ve queue_root AppSettings.PROCESS_MASTER_ROOT_DIR altındaki tam yollar olacak
    project_root_for_analysis = os.path.join(AppSettings.PROCESS_MASTER_ROOT_DIR, selected_process_folder_name)
    queue_root_for_analysis = os.path.join(AppSettings.PROCESS_MASTER_ROOT_DIR, selected_process_folder_name)

    if not os.path.exists(project_root_for_analysis):
        return f"Süreç klasörü bulunamadı: {project_root_for_analysis}", 500

    try:
        print(f"Analiz başlatılıyor: {selected_process_folder_name} (Gün Limiti: {day_limit_enabled}, Gün Sayısı: {day_limit_days})")

        # HTML dosyasının adını ve tam yolunu belirle
        safe_process_name = "".join(c for c in selected_process_folder_name if c.isalnum() or c in (' ', '.', '_')).replace(' ', '_')
        output_html_filename = f"hata_analizi_grafigi_{safe_process_name}_selector_detayli.html"
        html_output_full_path = os.path.join(AppSettings.REPORT_OUTPUT_DIR, output_html_filename)

        # run_analysis'i çağır, output_file_path'i de gönderiyoruz
        df_matched_results = run_analysis(
            process_name=selected_process_folder_name,
            day_limit_enabled=day_limit_enabled,
            day_limit_days=day_limit_days,
            use_ai=False, # AI kullanımı şu an için kapalı
            project_root=project_root_for_analysis,
            queue_root=queue_root_for_analysis,
            output_file_path=html_output_full_path # <-- BURASI ÖNEMLİ: main.py'ye gönderiliyor!
        )

        # HTML dosyasının varlığını kontrol et ve aç
        if os.path.exists(html_output_full_path):
            webbrowser.open_new_tab(f"file:///{html_output_full_path}")
            return f"Analiz tamamlandı. Grafik '{output_html_filename}' olarak oluşturuldu ve tarayıcınızda açılıyor."
        else:
            return "Analiz tamamlandı ancak grafik dosyası bulunamadı. Lütfen Output dizinini kontrol edin veya 'main.py' dosyasının grafiği doğru kaydettiğinden emin olun.", 500

    except Exception as e:
        import traceback
        traceback.print_exc() # Detaylı hata çıktısı için
        return f"Analiz sırasında bir hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    # Flask sunucusunun başlaması için kısa bir gecikme
    time.sleep(1)
    # Uygulama başlatıldığında varsayılan tarayıcıda tek bir sekme açar
    webbrowser.open_new_tab("http://127.0.0.1:5000")

    # Flask geliştirme sunucusunu debug modunda başlat, otomatik yeniden yükleyiciyi kapat.
    # use_reloader=False aynı zamanda tarayıcı açma davranışını da etkiler ve çift açılmayı engeller.
    app.run(debug=True, use_reloader=False)