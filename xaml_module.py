# xaml_module.py
import os
import pandas as pd
import xml.etree.ElementTree as ET
from config.settings import AppSettings # Yeni yapılandırma dosyamızdan import

def extract_xaml_activities(folder_path: str = AppSettings.PROJECT_FOLDER_PATH) -> pd.DataFrame:
    """
    Belirtilen klasördeki tüm XAML dosyalarını okur ve aktivite bilgilerini çıkarır.
    """
    activity_data = []
    print(f"[XAML] '{folder_path}' klasöründeki XAML dosyaları taranıyor...")

    for root_dir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xaml"):
                xaml_path = os.path.join(root_dir, file)
                try:
                    tree = ET.parse(xaml_path)
                    root = tree.getroot()

                    # Namespace'leri daha dinamik yakala
                    # Eğer XML'de default namespace varsa, ElementTree prefix olmadan işleyebilir.
                    # Ancak XPath sorguları için namespace'leri belirlemek daha güvenlidir.
                    # Örnek: {'ns': "http://schemas.microsoft.com/netfx/2009/xaml/activities"}
                    
                    # Tüm elementler üzerinde iterate et
                    for elem in root.iter():
                        tag = elem.tag.split('}')[-1] # Element tag'ini namespace olmadan al
                        display_name = elem.attrib.get('DisplayName')
                        selector = None

                        # 'Target' elementini doğrudan çocuklarından veya alt soyundan ara
                        # ElementTree'nin findall metodu, belirtilen tag'e sahip tüm çocukları/torunları bulur.
                        # `.{*}Target` herhangi bir namespace altındaki 'Target' tag'ini arar.
                        for target_elem in elem.findall('.//{*}Target'): 
                            if "Selector" in target_elem.attrib:
                                selector = target_elem.attrib["Selector"]
                                break # İlk bulunan selector yeterli

                        # Yalnızca DisplayName ve geçerli Selector'ı olan, belirli tiplerde olmayan aktiviteleri kaydet
                        if (display_name and 
                            selector and 
                            selector != '{x:Null}' and 
                            tag not in ["IfElseIf", "Sequence", "UiElementExists", "ForEachFileX", "TryCatch", "RetryScope"]):
                            
                            activity_data.append({
                                "XAML_File": os.path.basename(xaml_path), # Sadece dosya adını kaydet
                                "Activity_Type": tag,
                                "DisplayName": display_name,
                                "Selector": selector
                            })

                except ET.ParseError:
                    print(f"[XAML Parse Hatası] '{xaml_path}' dosyası parse edilemedi. Atlanıyor.")
                except Exception as e:
                    print(f"[XAML Genel Hata] '{xaml_path}' işlenirken hata oluştu: {e}")

    df = pd.DataFrame(activity_data)

    if not df.empty:
        # Son bir kontrol: DisplayName ve Selector'ın null olmadığından emin ol
        df = df[df['DisplayName'].notnull() & df['Selector'].notnull()].copy()
        
        # Selector'a göre duplicate'leri at. Bu, her bir benzersiz selector'ın
        # XAML'de bir "kaynağı" olduğu varsayımına dayanır.
        df.drop_duplicates(subset=['Selector'], inplace=True)
        print(f"[XAML] Sonuç DataFrame boyutu: {len(df)} kayıt.")
    else:
        print("[XAML] Hiçbir XAML aktivitesi bulunamadı veya filtrelendi.")

    return df