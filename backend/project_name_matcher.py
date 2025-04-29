# backend/project_name_matcher.py

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 2025
@author: asil.senel
"""


# backend/project_name_matcher.py

import os
from backend.config_backend import PROJECT_ROOT_PATH, QUEUE_ROOT_PATH
from rapidfuzz import fuzz

def list_all_projects():
    """Project klasörlerinin isimlerini listeler."""
    projects = []
    for item in os.listdir(PROJECT_ROOT_PATH):
        item_path = os.path.join(PROJECT_ROOT_PATH, item)
        if os.path.isdir(item_path):
            projects.append(item)
    return projects

def find_best_matches(process_name: str):
    """Seçilen süreç adına göre proje ve queue dosyası eşleşmesi yapar."""
    project_folders = os.listdir(PROJECT_ROOT_PATH)
    queue_files = os.listdir(QUEUE_ROOT_PATH)

    best_project = None
    best_queue = None
    best_project_score = 0
    best_queue_score = 0

    for project in project_folders:
        score = fuzz.ratio(process_name.lower(), project.lower())
        if score > best_project_score:
            best_project_score = score
            best_project = project

    for queue in queue_files:
        score = fuzz.ratio(process_name.lower(), queue.lower())
        if score > best_queue_score:
            best_queue_score = score
            best_queue = queue

    return {
        "project_folder_path": os.path.join(PROJECT_ROOT_PATH, best_project) if best_project else None,
        "queue_file_path": os.path.join(QUEUE_ROOT_PATH, best_queue) if best_queue else None,
        "project_match_score": best_project_score,
        "queue_match_score": best_queue_score
    }
