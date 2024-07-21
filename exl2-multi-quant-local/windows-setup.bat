@echo off

setlocal

REM check if "venv" subdirectory exists, if not, create one
set reinst=n
if not exist "venv\" (
    python -m venv venv
    set newvenv=y
) else (
    set /p reinst="venv directory already exists. Looking to upgrade/reinstall exllama? (will reinstall python venv) (y/n) "
)
if "%reinst%"=="y" (
    rmdir /s /q venv
    python -m venv venv
) else if not "%newvenv%"=="y" (
    exit
)

REM ask if the user has git installed
set /p gitwget="Do you have git and wget installed? (y/n) "

if "%gitwget%"=="y" (
    echo Setting up environment
) else (
    echo Please install git and wget before running this script.
    echo winget install wget git.git
    pause
    exit
)

REM ask for exllamav2 version
set /p exllamav2_version="Would you like to build stable or dev version of exllamav2? (stable, dev): "
if not "%exllamav2_version%"=="stable" if not "%exllamav2_version%"=="dev" (
    echo Invalid exllamav2 version. Please enter stable or dev.
    pause
    exit
)

REM if CUDA version 12 install pytorch for 12.1, else if CUDA 11 install pytorch for 11.8
echo CUDA compilers:
where nvcc
set /p cuda_version="Please enter your CUDA version (11 or 12): "

REM ask to install flash attention
echo Flash attention is a feature that could fix overflow issues on some more broken models, however, it will increase install time by a few hours.
set /p flash_attention="Would you like to install flash-attention? (rarely needed and optional) (y/n) "
if not "%flash_attention%"=="y" if not "%flash_attention%"=="n" (
    echo Invalid input. Please enter y or n.
    pause
    exit
)

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

echo Deleting potential conflicting files
del convert-to-safetensors.py
del download-model.py
rmdir /s /q exllamav2
del start-quant.bat
del enter-venv.bat

REM download stuff
echo Downloading files...
if "%exllamav2_version%"=="stable" (
    git clone https://github.com/turboderp/exllamav2
) else if "%exllamav2_version%"=="dev" (
    git clone https://github.com/turboderp/exllamav2 -b dev
)
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/convert-to-safetensors.py
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/download-model.py

echo Installing pip packages...

venv\scripts\python.exe -m pip install -r exllamav2/requirements.txt
venv\scripts\python.exe -m pip install huggingface-hub transformers accelerate
venv\scripts\python.exe -m pip install .\exllamav2

echo Writing batch files...

REM create start-quant-windows.bat
echo @echo off > start-quant.bat
echo venv\scripts\python.exe exl2-quant.py >> start-quant.bat
echo REM tada sound for fun >> start-quant.bat
echo powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\tada.wav").PlaySync(); >> start-quant.bat
echo pause >> start-quant.bat

REM create enter-venv.bat
echo @echo off > enter-venv.bat
echo cmd /k call venv\scripts\activate.bat >> enter-venv.bat

if "%flash_attention%"=="y" (
    echo Going to attempt to install flash attention but it isn't required.
    echo You may close now if you'd like and continue without flash attention.
    pause
    echo Get some popcorn and watch a movie. This will take a while.
    echo Installing flash-attn...
    venv\scripts\python.exe -m pip install git+https://github.com/Dao-AILab/flash-attention.git
)

powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\tada.wav").PlaySync();
echo Environment setup complete. run start-quant.bat to start the quantization process.
pause
