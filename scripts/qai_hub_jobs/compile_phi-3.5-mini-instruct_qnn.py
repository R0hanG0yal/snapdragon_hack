# Qualcomm AI Hub Compilation Job for phi-3.5-mini-instruct
# Target: Snapdragon X Elite (HP OmniBook X / Ultra)
import qai_hub as hub

# 1. Select target hardware
device = hub.Device("Snapdragon X Elite CRD")
print(f"Targeting Qualcomm Device: {device.name}")

# 2. Load model from Qualcomm AI Hub Model Zoo
model_name = "phi-3.5-mini-instruct"
print(f"Submitting compilation for {model_name} (Target: Hexagon NPU HTP v75)...")

# 3. Submit compile job targeting QNN Context Binary (NPU acceleration)
compile_job = hub.submit_compile_job(
    model=model_name,
    device=device,
    options="--target_runtime qnn_lib_context --quantize awq_int4_with_htp_context"
)
print(f"Compile Job Submitted: ID={compile_job.job_id}")

# 4. Profile latency and memory on real Snapdragon X Elite hardware
profile_job = hub.submit_profile_job(
    model=compile_job.get_target_model(),
    device=device
)
print("Profiling completed. Downloading optimized QNN ONNX bundle...")
target_model = compile_job.get_target_model()
target_model.download("phi-3.5-mini-instruct_snapdragon_x_elite.onnx")
print("Model ready for ONNX Runtime with QNNExecutionProvider!")
