# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 19:48:41 2025

@author: asil.senel
"""

# visualization_module.py

import plotly.express as px

def visualize_matched_selectors(df_matched):
    if df_matched.empty:
        print("⚠️ Görselleştirilecek eşleşme bulunamadı.")
        return

    # Selector bazlı sayım
    df_grouped = df_matched.groupby(['Selector', 'DisplayName']).size().reset_index(name='Count')

    # Grafik oluştur
    fig = px.bar(
        df_grouped,
        x='DisplayName',
        y='Count',
        hover_data=['Selector'],  # Mouse ile üzerine gelince selector görünsün
        title='Matched UI Selectors by Display Name',
    )

    
    fig.show(renderer="browser")
