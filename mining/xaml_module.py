# xaml_module.py

import os
import pandas as pd
import xml.etree.ElementTree as ET
# PROJECT_FOLDER_PATH artık config'den doğrudan alınmıyor, argüman olarak gelecek.
# from mining_main.config_mining import PROJECT_FOLDER_PATH

# folder_path artık zorunlu bir argüman
def extract_xaml_activities(folder_path: str):
    print(f"[XAML] Klasörden XAML aktiviteleri çıkarılıyor: {folder_path}")
    activity_data = []

    if not os.path.isdir(folder_path):
        print(f"[XAML Error] Belirtilen XAML klasörü bulunamadı: {folder_path}")
        # Boş DataFrame veya hata döndürebilirsiniz. Burada boş döndürüyoruz.
        return pd.DataFrame(columns=["XAML_File", "Activity_Type", "DisplayName", "Selector"])


    for root_dir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xaml"):
                xaml_path = os.path.join(root_dir, file)
                try:
                    tree = ET.parse(xaml_path)
                    root = tree.getroot()

                    for elem in root.iter():
                        tag = elem.tag.split('}')[-1]
                        display_name = elem.attrib.get('DisplayName')
                        selector = None

                        # Selector bilgisi Target elementinin içinde saklı
                        for child in elem.iter():
                            child_tag = child.tag.split('}')[-1]
                            if child_tag == "Target":
                                # Target elementinin attrib'lerinde Selector'u ara
                                selector = child.attrib.get("Selector")
                                # Eğer Target içinde bir <ui:Selector> elementi varsa
                                if selector is None:
                                     selector_element = child.find('.//{*}Selector')
                                     if selector_element is not None:
                                         selector = selector_element.text

                                # Selector bulunduysa bu döngüden çıkabiliriz
                                if selector:
                                     break


                        # Sadece DisplayName veya Selector'u olan aktiviteleri eklemek daha anlamlı olabilir
                        # veya tüm elemanları toplayıp sonra filtrelemek
                        # Mevcut mantığınız tüm elemanları ekleyip sonra filtreliyor, devam edelim.
                        activity_data.append({
                            "XAML_File": xaml_path,
                            "Activity_Type": tag,
                            "DisplayName": display_name,
                            "Selector": selector # Selector None olabilir
                        })

                except ET.ParseError:
                    print(f"[XAML Parse Error] Dosya okunamadı veya XML hatası: {xaml_path}")
                except Exception as e:
                    print(f"[XAML Processing Error] Dosya işlenirken hata oluştu {xaml_path}: {e}")


    df = pd.DataFrame(activity_data)

    # DataFrame boşsa filtrelemeye çalışmadan boş döndür
    if df.empty:
        print("[XAML] Hiç aktivite bulunamadı veya parse hatası oluştu.")
        return pd.DataFrame(columns=["XAML_File", "Activity_Type", "DisplayName", "Selector"])


    # Filtreleme adımları (mevcut mantığınızı koruyoruz)
    print(f"[XAML] Toplam {len(df)} eleman bulundu. Filtreleme uygulanıyor...")

    # DisplayName ve Selector null olmayanları seç
    df = df[df['DisplayName'].notnull() & df['Selector'].notnull()]
    print(f"[XAML] DisplayName ve Selector olan kayıtlar: {len(df)}")

    # Selector'u "{x:Null}" olmayanları seç
    df = df[df['Selector'] != '{x:Null}']
    print(f"[XAML] Selectoru {{x:Null}} olmayan kayıtlar: {len(df)}")

    # Belirli Activity_Type'ları hariç tut
    excluded_activity_types = ["IfElseIf", "Sequence", "UiElementExists", "ForEachFileX", "TryCatch", "RetryScope"]
    df = df[~df['Activity_Type'].isin(excluded_activity_types)]
    print(f"[XAML] Hariç tutulan Activity Type'lardan sonra kalan kayıtlar: {len(df)}")

    # Selector bazında duplicate kayıtları kaldır
    initial_len = len(df)
    df = df.drop_duplicates(subset=['Selector'])
    print(f"[XAML] Selector bazında duplicate'ler kaldırıldı. Kalan kayıtlar: {len(df)} (kaldırılan: {initial_len - len(df)})")


    return df
