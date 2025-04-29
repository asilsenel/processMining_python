# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:57:11 2025

@author: asil.senel
"""
# backend/api_server.py

from fastapi import FastAPI
from pydantic import BaseModel
from backend.project_name_matcher import resolve_paths
from config import PROJECT_ROOT_PATH, QUEUE_ROOT_PATH

app = FastAPI()

class AnalyzeRequest(BaseModel):
    process_name: str
    day_limit_enabled: bool
    day_limit_days: int
    use_ai: bool

@app.get("/")
async def root():
    return {"message": "API çalışıyor!"}

@app.post("/start-analysis")
async def analyze_process(request: AnalyzeRequest):
    print("🔍 Eşleştirme başlatıldı...")

    resolved = resolve_paths(
        process_name=request.process_name,
        project_root=PROJECT_ROOT_PATH,
        queue_root=QUEUE_ROOT_PATH
    )

    if "error" in resolved:
        return {"error": resolved["error"]}

    print(f"✅ Proje klasörü: {resolved['project_path']}")
    print(f"✅ CSV dosyası: {resolved['csv_path']}")

    # Şimdilik sadece geri dön
    return {
        "message": f"Analiz başladı: {request.process_name}",
        "project_path": resolved["project_path"],
        "csv_path": resolved["csv_path"]
    }
