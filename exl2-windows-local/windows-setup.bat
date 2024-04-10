@echo off

setlocal

REM check if "venv" subdirectory exists, if not, create one
if not exist "venv\" (
    python -m venv venv
) else (
    echo venv directory already exists. If something is broken, delete everything but exl2-quant.py and run this script again.
    pause
    exit
)

REM ask if the user has git installed
set /p gitinst="Do you have git installed? (y/n) "

if "%gitinst%"=="y" (
    echo Setting up environment
) else (
    echo Please install git before running this script.
    pause
    exit
)

REM if CUDA version 12 install pytorch for 12.1, else if CUDA 11 install pytorch for 11.8
echo CUDA path: %CUDA_HOME%
set /p cuda_version="Please enter your CUDA version (11 or 12): "

if "%cuda_version%"=="11" (
    echo Installing PyTorch for CUDA 11.8...
    venv\scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu118 -q --upgrade
) else if "%cuda_version%"=="12" (
    echo Installing PyTorch for CUDA 12.1...
    venv\scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu121 -q --upgrade
) else (
    echo Invalid CUDA version. Please enter 11 or 12.
    pause
    exit
)

REM download stuff
echo Downloading files...
git clone https://github.com/turboderp/exllamav2

echo Installing pip packages...

venv\scripts\python.exe -m pip install -r exllamav2/requirements.txt -q
venv\scripts\python.exe -m pip install huggingface-hub -q
venv\scripts\python.exe -m pip install .\exllamav2 -q

move "download multiple models.ps1" exllamav2
move convert-model-auto.bat exllamav2
move download-model.py exllamav2
move venv exllamav2

powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\tada.wav").PlaySync();
echo Environment setup complete. Read instructions.txt for further instructions.
pause