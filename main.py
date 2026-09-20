"""
OmniCognition NPU - Main Unified Entry Point
Snapdragon AI Lab Build & Present Challenge 2026
Author: Rohan Goyal (rohangoyal5127@gmail.com)
"""

import sys
import argparse
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.hardware import HardwareManager
from core.ai_hub import AIHubModelManager
from core.telemetry import TelemetryEngine
from ui.app import start_server

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(force_terminal=True, legacy_windows=False)

def display_banner():
    banner_text = """==================================================================
           OMNICOGNITION NPU - SNAPDRAGON AI LAB
   Qualcomm Hexagon NPU 45 TOPS Intelligence for HP OmniBook X
=================================================================="""
    console.print(Panel(banner_text, subtitle="[cyan]Qualcomm AI Lab Build & Present Challenge 2026 | Rohan Goyal[/cyan]", expand=False))

def run_diagnostics():
    hw = HardwareManager()
    tel = TelemetryEngine()
    hub = AIHubModelManager()
    
    display_banner()
    
    # 1. Hardware Status Table
    hw_status = hw.get_hardware_status()
    table = Table(title="💻 Snapdragon Hardware Diagnostic", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="dim", width=24)
    table.add_column("Detected Specification", style="bold green")
    
    table.add_row("Target Laptop", hw_status["device"])
    table.add_row("NPU Compute Engine", hw_status["npu_engine"])
    table.add_row("Peak AI TOPS", f"{hw_status['rated_tops']} TOPS")
    table.add_row("Active Execution Provider", hw_status["active_provider"])
    table.add_row("NPU Active Inference TDP", f"{hw_status['power_efficiency']['npu_draw_watts']} Watts")
    table.add_row("Discrete GPU Baseline TDP", f"{hw_status['power_efficiency']['gpu_draw_watts']} Watts")
    table.add_row("Energy Savings Ratio", hw_status["power_efficiency"]["energy_savings_ratio"])
    console.print(table)

    # 2. Qualcomm AI Hub Models Table
    models_table = Table(title="📦 Qualcomm AI Hub Model Optimization Catalog", show_header=True, header_style="bold cyan")
    models_table.add_column("Model Key", style="bold")
    models_table.add_column("Category", style="dim")
    models_table.add_column("Precision", style="yellow")
    models_table.add_column("NPU Latency", style="green")
    models_table.add_column("CPU Latency", style="red")
    models_table.add_column("Speedup", style="bold green")

    for key, val in hub.get_catalog().items():
        models_table.add_row(
            key,
            val["category"],
            val["precision"],
            f"{val['latency_ms_npu']} ms",
            f"{val['latency_ms_cpu']} ms",
            val["speedup"]
        )
    console.print(models_table)

    # 3. Generate compilation scripts for reproducibility
    hub.save_compilation_scripts("scripts/qai_hub_jobs")
    console.print("[green]✔ Generated Qualcomm AI Hub compilation jobs in [bold]scripts/qai_hub_jobs/[/bold][/green]")

def main():
    parser = argparse.ArgumentParser(description="OmniCognition NPU - Snapdragon AI Lab Challenge")
    parser.add_argument("--diag", action="store_true", help="Run system hardware diagnostics and AI Hub model verification")
    parser.add_argument("--serve", action="store_true", default=True, help="Launch interactive web dashboard (Default)")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind dashboard server")
    args = parser.parse_args()

    if args.diag:
        run_diagnostics()
    else:
        display_banner()
        console.print(f"[bold green]🚀 Launching OmniCognition NPU Dashboard on http://127.0.0.1:{args.port}[/bold green]")
        console.print("[dim]Press Ctrl+C to stop.[/dim]")
        start_server(port=args.port)

if __name__ == "__main__":
    main()
