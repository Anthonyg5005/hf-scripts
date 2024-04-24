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
set /p gitwget="Do you have git and wget installed? (y/n) "

if "%gitwget%"=="y" (
    echo "Setting up environment"
) else (
    echo Please install git and wget before running this script.
    echo winget install wget
    echo winget install git
    pause
    exit
)

REM if CUDA version 12 install pytorch for 12.1, else if CUDA 11 install pytorch for 11.8
echo CUDA path: %CUDA_HOME%
set /p cuda_version="Please enter your CUDA version (11 or 12): "

if "%cuda_version%"=="11" (
    echo Installing PyTorch for CUDA 11.8...
    venv\scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu118 --upgrade
) else if "%cuda_version%"=="12" (
    echo Installing PyTorch for CUDA 12.1...
    venv\scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu121 --upgrade
) else (
    echo Invalid CUDA version. Please enter 11 or 12.
    pause
    exit
)

REM download stuff
echo Downloading files...
git clone https://github.com/turboderp/exllamav2
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/convert-to-safetensors.py
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/download-model.py

echo Installing pip packages...

venv\scripts\python.exe -m pip install -r exllamav2/requirements.txt
venv\scripts\python.exe -m pip install huggingface-hub transformers accelerate
venv\scripts\python.exe -m pip install .\exllamav2

REM create start-quant-windows.bat
echo @echo off > start-quant.bat
echo venv\scripts\python.exe exl2-quant.py >> start-quant.bat
echo REM tada sound for fun >> start-quant.bat
echo powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\tada.wav").PlaySync(); >> start-quant.bat
echo pause >> start-quant.bat
powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\tada.wav").PlaySync();
echo Environment setup complete. run start-quant.bat to start the quantization process.
pause
