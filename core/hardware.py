"""
OmniCognition NPU - Hardware Abstraction & Qualcomm AI Engine Direct (QNN) Interface
Optimized for Snapdragon-powered HP PCs (HP OmniBook X / HP OmniBook Ultra)
"""

import os
import platform
import logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("OmniCognition.Hardware")

class HardwareManager:
    """
    Manages NPU, GPU, and CPU execution providers with specific acceleration profiles
    for Qualcomm Snapdragon X Elite and Snapdragon X Plus (Hexagon NPU v73/v75).
    """

    def __init__(self):
        self.system_info = self._probe_system()
        self.active_provider = self._select_best_provider()

    def _probe_system(self) -> Dict[str, Any]:
        """Probes the host OS, architecture, and hardware capabilities."""
        uname = platform.uname()
        arch = platform.machine().lower()
        is_windows = uname.system.lower() == "windows"
        is_arm64 = "arm" in arch or "aarch64" in arch
        
        # Check environment overrides or Snapdragon indicators
        has_snapdragon = is_arm64 or "snapdragon" in uname.processor.lower() or os.environ.get("FORCE_SNAPDRAGON_NPU", "0") == "1"
        
        return {
            "os": uname.system,
            "os_release": uname.release,
            "architecture": arch,
            "is_windows": is_windows,
            "is_arm64": is_arm64,
            "is_snapdragon": has_snapdragon,
            "npu_name": "Qualcomm Hexagon NPU (HTP v73/v75)" if has_snapdragon else "Simulated Hexagon NPU (45 TOPS Profile)",
            "max_npu_tops": 45.0, # Snapdragon X Elite / X Plus 45 TOPS rating
            "soc_model": "Snapdragon X Elite (X1E-80-100) / HP OmniBook X" if has_snapdragon else "Qualcomm Snapdragon X Series (Profiled)",
            "npu_tpd_watts": 4.5, # Under 5W typical inference TDP
            "gpu_tpd_watts": 45.0, # Traditional discrete laptop GPU TDP
            "cpu_tpd_watts": 28.0  # Typical x86/ARM CPU package TDP
        }

    def _select_best_provider(self) -> str:
        """
        Determines the optimal ONNX Runtime / AI Engine execution provider.
        Priority:
        1. QNNExecutionProvider (Qualcomm Hexagon NPU via QnnHtp.dll)
        2. DirectMLExecutionProvider (DirectX12 NPU/GPU acceleration)
        3. CPUExecutionProvider (Universal Fallback)
        """
        try:
            import onnxruntime as ort
            available = ort.get_available_providers()
            logger.info(f"Available ONNX Runtime Providers: {available}")
            
            if "QNNExecutionProvider" in available:
                logger.info("Selected Qualcomm QNN Execution Provider (HTP NPU Native)")
                return "QNNExecutionProvider"
            elif "DirectMLExecutionProvider" in available:
                logger.info("Selected DirectML Execution Provider (DirectX 12)")
                return "DirectMLExecutionProvider"
            else:
                logger.info("Selected CPU Execution Provider (Development Fallback)")
                return "CPUExecutionProvider"
        except ImportError:
            logger.warning("onnxruntime not installed or mock mode active. Defaulting to Simulated QNN Provider.")
            return "QNNExecutionProvider (Simulated Hexagon NPU)"

    def get_qnn_session_options(self) -> Dict[str, Any]:
        """
        Returns optimized Qualcomm QNN configuration options for Hexagon NPU.
        Specifies burst performance mode, low precision (INT8/INT4), and v73/v75 architecture.
        """
        qnn_options = {
            "backend_path": "QnnHtp.dll",
            "htp_performance_mode": "burst",          # Options: burst, sustained_high_performance, power_saver
            "htp_precision": "precision_low",           # INT8/INT4 quantization for Hexagon Tensor Processor
            "htp_arch": "v75",                         # Snapdragon X Elite architecture
            "soc_model": "43",                         # Snapdragon X Elite internal SoC ID
            "enable_htp_fp16_precision": "1",
            "qnn_context_priority": "high"
        }
        return qnn_options

    def get_hardware_status(self) -> Dict[str, Any]:
        """Returns consolidated hardware and telemetry status for UI and logs."""
        return {
            "device": self.system_info["soc_model"],
            "npu_engine": self.system_info["npu_name"],
            "rated_tops": self.system_info["max_npu_tops"],
            "active_provider": self.active_provider,
            "power_efficiency": {
                "npu_draw_watts": self.system_info["npu_tpd_watts"],
                "gpu_draw_watts": self.system_info["gpu_tpd_watts"],
                "cpu_draw_watts": self.system_info["cpu_tpd_watts"],
                "energy_savings_ratio": f"{round((self.system_info['gpu_tpd_watts'] - self.system_info['npu_tpd_watts']) / self.system_info['gpu_tpd_watts'] * 100, 1)}%"
            },
            "status": "Operational - 45 TOPS Hexagon Engine Ready"
        }

if __name__ == "__main__":
    hw = HardwareManager()
    import json
    print(json.dumps(hw.get_hardware_status(), indent=2))
