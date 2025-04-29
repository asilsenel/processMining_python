# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 19:04:32 2025

@author: asil.senel
"""
# matching_module.py

from rapidfuzz import fuzz
import pandas as pd

def match_selectors(df_xaml, df_csv, threshold=90):
    """
    CSV'den gelen selectorları XAML'den gelen selectorlarla fuzzy matching yapar.
    threshold: 0-100 arası benzerlik eşiği.
    """
    matched_records = []

    for idx, row in df_csv.iterrows():
        selector_csv = row['Selector']
        best_score = 0
        best_match = None

        for idx_xaml, row_xaml in df_xaml.iterrows():
            selector_xaml = row_xaml['Selector']
            score = fuzz.ratio(selector_csv, selector_xaml)

            if score > best_score:
                best_score = score
                best_match = row_xaml

        if best_score >= threshold and best_match is not None:
            matched_records.append({
                "Selector": selector_csv,
                "Activity_Type": best_match["Activity_Type"],
                "DisplayName": best_match["DisplayName"]
            })

    df_matched = pd.DataFrame(matched_records)
    return df_matched
