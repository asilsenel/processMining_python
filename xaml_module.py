# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 18:23:29 2025

@author: asil.senel
"""

# xaml_module.py

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 15:55:23 2025

@author: asil.senel
"""

import os
import pandas as pd
import xml.etree.ElementTree as ET
from config import PROJECT_FOLDER_PATH

def extract_xaml_activities(folder_path=PROJECT_FOLDER_PATH):
    activity_data = []

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

                        for child in elem.iter():
                            child_tag = child.tag.split('}')[-1]
                            if child_tag == "Target" and "Selector" in child.attrib:
                                selector = child.attrib["Selector"]
                                break

                        activity_data.append({
                            "XAML_File": xaml_path,
                            "Activity_Type": tag,
                            "DisplayName": display_name,
                            "Selector": selector
                        })

                except ET.ParseError:
                    print(f"[XAML Parse Error] {xaml_path}")

    df = pd.DataFrame(activity_data)

    if not df.empty:
        df['Has_DisplayName'] = df['DisplayName'].notna() & df['DisplayName'].astype(str).str.strip().ne('')
        df['Has_Selector'] = df['Selector'].notna() & df['Selector'].astype(str).str.strip().ne('')
        df = df[df['DisplayName'].notnull()]
        df = df[df['Selector'].notnull()]
        df = df[df['Selector'] != '{x:Null}']
        df = df[~df['Activity_Type'].isin(["IfElseIf", "Sequence", "UiElementExists", "ForEachFileX", "TryCatch", "RetryScope"])]
        df = df.drop_duplicates(subset=['Selector'])

    return df
