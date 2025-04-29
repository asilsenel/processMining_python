# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 08:48:14 2025

@author: asil.senel
"""

# backend/project_name_matcher.py

from pathlib import Path
from rapidfuzz import fuzz

def find_best_match(process_name: str, candidates: list, threshold: int = 80) -> str:
    best_match = ""
    best_score = 0
    for candidate in candidates:
        score = fuzz.partial_ratio(process_name.lower(), candidate.lower())
        if score > best_score:
            best_score = score
            best_match = candidate
    return best_match if best_score >= threshold else None

def resolve_paths(process_name: str, project_root: str, queue_root: str):
    project_root = Path(project_root)
    queue_root = Path(queue_root)

    project_dirs = [f.name for f in project_root.iterdir() if f.is_dir()]
    queue_files = [f.name for f in queue_root.glob("*.csv")]

    matched_project = find_best_match(process_name, project_dirs)
    matched_csv = find_best_match(process_name, queue_files)

    if matched_project and matched_csv:
        return {
            "project_path": str(project_root / matched_project),
            "csv_path": str(queue_root / matched_csv)
        }
    else:
        return {
            "error": "Eşleşen proje klasörü veya CSV dosyası bulunamadı."
        }
