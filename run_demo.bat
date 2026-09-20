@echo off
title OmniCognition NPU - Snapdragon AI Lab Challenge
echo ==================================================================
echo           OMNICOGNITION NPU - SNAPDRAGON AI LAB
echo    Qualcomm Hexagon NPU 45 TOPS Intelligence for HP OmniBook X
echo ==================================================================
echo.
echo Running automated diagnostics...
python main.py --diag
echo.
echo Launching Interactive Dashboard on http://127.0.0.1:8080...
start http://127.0.0.1:8080
python main.py --serve
pause
