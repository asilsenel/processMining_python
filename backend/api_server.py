# backend/api_server.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from backend.config_backend import PROJECT_ROOT_PATH, QUEUE_ROOT_PATH
from backend.project_name_matcher import list_all_projects, find_best_matches

# Mining klasörünü Python yoluna ekle
mining_path = r"C:/Users/asil.senel/Desktop/Kişisel/Python/Process Mining"
sys.path.append(mining_path)

# Artık mining modüllerini içe aktarabiliriz
from main import run_analysis

app = FastAPI()

# CORS izinleri (Streamlit için şart)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API MODELLERİ
class AnalyzeRequest(BaseModel):
    process_name: str
    day_limit_enabled: bool
    day_limit_days: int
    use_ai: bool

@app.get("/")
def root():
    return {"message": "API çalışıyor!"}

@app.get("/get-paths")
def get_project_names():
    return {"projects": list_all_projects(PROJECT_ROOT_PATH, QUEUE_ROOT_PATH)}

@app.post("/analyze")
def analyze_process(request: AnalyzeRequest):
    print("🎯 Analiz başlıyor...")
    run_analysis(
        process_name=request.process_name,
        day_limit_enabled=request.day_limit_enabled,
        day_limit_days=request.day_limit_days,
        use_ai=request.use_ai,
        project_root=PROJECT_ROOT_PATH,
        queue_root=QUEUE_ROOT_PATH
        )
    return {"message": f"✅ Analiz tamamlandı: {request.process_name}"}
