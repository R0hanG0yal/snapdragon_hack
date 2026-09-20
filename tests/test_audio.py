"""
Unit tests for Whisper-NPU Audio & Meeting Copilot.
"""

import pytest
from audio.speech_copilot import SpeechCopilot

def test_audio_transcribe_and_analyze():
    copilot = SpeechCopilot()
    result = copilot.transcribe_and_analyze("demo_meeting")
    
    assert result["status"] == "success"
    assert len(result["transcript"]) > 0
    assert "Snapdragon" in result["full_transcript_text"]
    assert len(result["executive_summary"]) > 20
    assert len(result["action_items"]) > 0
    assert result["latency_ms"] < 1000.0
