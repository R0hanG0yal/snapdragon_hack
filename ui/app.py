"""
OmniCognition NPU - FastAPI Application Server
Provides REST APIs and serves the real-time interactive dashboard.
"""

import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from core.hardware import HardwareManager
from core.ai_hub import AIHubModelManager
from core.telemetry import TelemetryEngine
from audio.speech_copilot import SpeechCopilot
from rag.neural_vault import NeuralVault
from vision.privacy_guard import OmniGuardVision

app = FastAPI(title="OmniCognition NPU Engine", version="1.0.0")

# Initialize core services
hardware_mgr = HardwareManager()
telemetry_eng = TelemetryEngine()
ai_hub_mgr = AIHubModelManager()
speech_copilot = SpeechCopilot(hardware=hardware_mgr, telemetry=telemetry_eng)
neural_vault = NeuralVault(hardware=hardware_mgr, telemetry=telemetry_eng)
vision_guard = OmniGuardVision(hardware=hardware_mgr, telemetry=telemetry_eng)

class QueryRequest(BaseModel):
    query: str

class DocumentRequest(BaseModel):
    title: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the main single-page application dashboard."""
    html_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/status")
async def get_system_status():
    """Returns hardware specs, active NPU provider, and power profile."""
    return hardware_mgr.get_hardware_status()

@app.get("/api/models")
async def get_model_catalog():
    """Returns the Qualcomm AI Hub model catalog."""
    return ai_hub_mgr.get_catalog()

@app.get("/api/audio/transcribe")
async def transcribe_audio():
    """Executes on-device speech-to-text and meeting summarization on NPU."""
    return speech_copilot.transcribe_and_analyze()

@app.post("/api/rag/query")
async def query_rag(request: QueryRequest):
    """Queries the local neural vault with semantic embeddings + SLM generation."""
    return neural_vault.query(request.query)

@app.post("/api/rag/add_document")
async def add_document(request: DocumentRequest):
    """Indexes a new document into the local neural vault."""
    return neural_vault.add_document(request.title, request.content)

@app.get("/api/vision/scan")
async def scan_vision(simulate_bystander: bool = Query(False)):
    """Runs on-device YOLO vision privacy scan for shoulder surfing."""
    return vision_guard.analyze_frame(simulate_bystander=simulate_bystander)

@app.get("/api/telemetry/benchmarks")
async def get_benchmarks():
    """Returns comparative benchmark data for NPU vs CPU vs GPU vs Cloud."""
    return telemetry_eng.get_benchmark_comparison()

def start_server(host: str = "127.0.0.1", port: int = 8080):
    """Starts the Uvicorn web server."""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
