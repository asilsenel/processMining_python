# visualization_module.py

import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def visualize_matched_selectors(df_matched: pd.DataFrame, process_name: str, output_file_path: str):
    """
    Eşleşen selector'ları veya analiz sonuçlarını görselleştirir ve belirtilen yola HTML dosyası olarak kaydeder.

    Args:
        df_matched (pd.DataFrame): Eşleşen selectorları veya analiz sonuçlarını içeren DataFrame.
        process_name (str): Analiz edilen sürecin adı. Grafiğin başlığında kullanılır.
        output_file_path (str): Oluşturulan HTML raporunun kaydedileceği tam dosya yolu.
    """
    print(f"🎨 '{process_name}' için görselleştirme başlatılıyor...")
    print(f"Grafik dosyası kaydedilecek yer: {output_file_path}")

    fig = go.Figure() # Boş bir figür ile başlıyoruz

    try:
        if df_matched.empty:
            print(f"❗ '{process_name}' için eşleşen veri bulunamadı. Boş bir grafik oluşturuluyor.")
            fig = go.Figure(layout=go.Layout(title=go.layout.Title(text=f"{process_name} - Grafik Oluşturulamadı (Veri Yok)")))
        else:
            # 'Matched_DisplayName' sütununda tekrar eden değerleri say
            if 'Matched_DisplayName' in df_matched.columns and 'Matched_XAML_Selector' in df_matched.columns:
                # Aynı DisplayName'e sahip farklı selector'ları gruplamak ve birleştirmek için
                # Her bir DisplayName için ilgili tüm benzersiz selectorları topluyoruz.
                grouped_data = df_matched.groupby('Matched_DisplayName').agg(
                    Error_Count=('Matched_DisplayName', 'count'),
                    All_Selectors=('Matched_XAML_Selector', lambda x: '<br>'.join(sorted(x.unique())))
                    # HTML'de yeni satır için <br> kullanıyoruz
                ).reset_index()

                # 'Error_Count' sütununa göre sırala ve en çok tekrar eden ilk N tanesini al
                top_n = 15
                data_for_plot = grouped_data.sort_values(by='Error_Count', ascending=False).head(top_n)

                if not data_for_plot.empty:
                    # Plotly Express ile bar grafik oluştur
                    fig = px.bar(data_for_plot, x='Matched_DisplayName', y='Error_Count',
                                 title=f"{process_name} - En Çok Hata Veren Aktiviteler ({len(data_for_plot)} Adet)",
                                 labels={'Matched_DisplayName': 'Aktivite Adı (DisplayName)', 'Error_Count': 'Hata Sayısı'},
                                 color_discrete_sequence=px.colors.qualitative.Pastel,
                                 hover_data={'All_Selectors': True, 'Error_Count': True}) # Hover'da tüm selectorları ve hata sayısını göster

                    fig.update_traces(
                        hovertemplate='<b>Aktivite Adı:</b> %{x}<br>'+
                                      '<b>Hata Sayısı:</b> %{y}<br>'+
                                      '<b>Selector(lar):</b> %{customdata[0]}<extra></extra>', # customdata[0] All_Selectors'ı temsil eder
                        customdata=data_for_plot[['All_Selectors']].values # customdata olarak All_Selectors sütununu geçiriyoruz
                    )

                    fig.update_layout(
                        xaxis_tickangle=-45,
                        xaxis_title="Aktivite Adı",
                        yaxis_title="Hata Sayısı",
                        height=600
                    )
                else:
                    fig = go.Figure(layout=go.Layout(title=go.layout.Title(text=f"{process_name} - Bar Grafik Oluşturulamadı (Yeterli Eşleşen Aktivite Verisi Yok)")))
            else:
                print("Uyarı: 'Matched_DisplayName' veya 'Matched_XAML_Selector' sütunu bulunamadı. Lütfen 'df_matched' DataFrame'inizin yapısını kontrol edin.")
                if not df_matched.empty:
                    # Alternatif olarak df_matched'ın ilk birkaç satırını tablo olarak göster
                    fig = go.Figure(data=[go.Table(
                        header=dict(values=list(df_matched.columns),
                                     fill_color='paleturquoise',
                                     align='left'),
                        cells=dict(values=[df_matched[col].head(5) for col in df_matched.columns],
                                       fill_color='lavender',
                                       align='left'))
                    ])
                    fig.update_layout(title_text=f"{process_name} - df_matched İlk 5 Satırı (Hedef Sütun Yok)")
                else:
                    fig = go.Figure(layout=go.Layout(title=go.layout.Title(text=f"{process_name} - Grafik Verisi Yok")))

    except Exception as e:
        print(f"HATA: '{process_name}' için görselleştirme kodu çalışırken hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        fig = go.Figure(layout=go.Layout(title=go.layout.Title(text=f"Hata Oluştu: Grafik Yüklenemedi - {e}")))

    # Çıktı klasörünü oluştur ve HTML dosyasını kaydet
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📂 Rapor klasörü oluşturuldu: {output_dir}")

    fig.write_html(output_file_path)
    print(f"✅ Grafik başarıyla kaydedildi: {output_file_path}")