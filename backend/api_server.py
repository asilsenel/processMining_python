# backend/api_server.py

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:57:11 2025
@author: asil.senel
"""

from fastapi import FastAPI
from pydantic import BaseModel
from backend.project_name_matcher import find_best_matches

app = FastAPI()

# İstek modelini tanımla
class AnalyzeRequest(BaseModel):
    process_name: str
    day_limit_enabled: bool
    day_limit_days: int
    use_ai: bool  # frontend'de AI Powered switch eklemiştik ya, onu da destekliyor

class FindPathsRequest(BaseModel):
    process_name: str

@app.get("/")
async def root():
    return {"message": "API çalışıyor!"}

@app.post("/analyze")
async def analyze_process(request: AnalyzeRequest):
    print("🚀 Gelen Parametreler: ")
    print(f"Process Name: {request.process_name}")
    print(f"Day Limit Enabled: {request.day_limit_enabled}")
    print(f"Day Limit Days: {request.day_limit_days}")
    print(f"Use AI: {request.use_ai}")

    # Buraya mining işlemleri bağlanacak ileride
    return {"message": f"Analiz başlatıldı: {request.process_name}"}

@app.post("/find-paths")
async def find_paths(request: FindPathsRequest):
    matches = find_best_matches(request.process_name)
    return matches
