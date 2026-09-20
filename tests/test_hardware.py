"""
Unit tests for Qualcomm Hexagon NPU Hardware Manager & QNN Configuration.
"""

import pytest
from core.hardware import HardwareManager

def test_hardware_detection():
    hw = HardwareManager()
    status = hw.get_hardware_status()
    
    assert "rated_tops" in status
    assert status["rated_tops"] == 45.0
    assert "power_efficiency" in status
    assert status["power_efficiency"]["npu_draw_watts"] < 5.0
    assert "active_provider" in status

def test_qnn_session_options():
    hw = HardwareManager()
    options = hw.get_qnn_session_options()
    
    assert options["backend_path"] == "QnnHtp.dll"
    assert options["htp_performance_mode"] == "burst"
    assert options["htp_arch"] == "v75"
