# backend/project_name_matcher.py

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 2025
@author: asil.senel
"""

import os
from rapidfuzz import fuzz, process
from config_backend import PROJECT_ROOT_PATH, QUEUE_ROOT_PATH

def find_best_matches(process_name):
    # --- 1. Tüm proje klasörlerini ve csv dosyalarını oku ---
    project_folders = [f for f in os.listdir(PROJECT_ROOT_PATH) if os.path.isdir(os.path.join(PROJECT_ROOT_PATH, f))]
    queue_files = [f for f in os.listdir(QUEUE_ROOT_PATH) if f.endswith(".csv")]

    # --- 2. En iyi proje klasörü eşleşmesini bul ---
    best_project_match, project_score = process.extractOne(process_name, project_folders, scorer=fuzz.partial_ratio)

    # --- 3. En iyi CSV dosya eşleşmesini bul ---
    best_queue_match, queue_score = process.extractOne(process_name, queue_files, scorer=fuzz.partial_ratio)

    # --- 4. Path'leri oluştur ---
    project_folder_path = os.path.join(PROJECT_ROOT_PATH, best_project_match) if best_project_match else None
    csv_file_path = os.path.join(QUEUE_ROOT_PATH, best_queue_match) if best_queue_match else None

    # --- 5. Sonuçları döndür ---
    return {
        "project_folder_path": project_folder_path,
        "csv_file_path": csv_file_path,
        "project_score": project_score,
        "queue_score": queue_score
    }
