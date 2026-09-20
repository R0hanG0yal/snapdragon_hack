"""
Unit tests for OmniGuard Vision Privacy Shield and Telemetry Engine.
"""

import pytest
from vision.privacy_guard import OmniGuardVision
from core.telemetry import TelemetryEngine

def test_vision_privacy_detection():
    guard = OmniGuardVision()
    
    # 1. Normal state
    normal_res = guard.analyze_frame(simulate_bystander=False)
    assert not normal_res["threat_detected"]
    assert normal_res["recommended_action"] == "MAINTAIN_NORMAL_DISPLAY"
    assert normal_res["primary_user"]["detected"]
    
    # 2. Threat state (shoulder surfing)
    threat_res = guard.analyze_frame(simulate_bystander=True)
    assert threat_res["threat_detected"]
    assert "BLUR" in threat_res["recommended_action"]
    assert threat_res["bystander"]["detected"]

def test_telemetry_metrics():
    telemetry = TelemetryEngine()
    bench = telemetry.get_benchmark_comparison()
    
    assert "speech_to_text_whisper" in bench
    assert "embedding_generation_minilm" in bench
    assert "overall_system_efficiency" in bench
    assert "4.2 Watts" in bench["overall_system_efficiency"]["npu_active_draw"]
