#!/bin/bash

# converted from windows-setup.bat by github copilot

# check if "venv" subdirectory exists, if not, create one
if [ ! -d "venv" ]; then
    python3 -m venv venv
else
    echo "venv directory already exists. If something is broken, delete venv folder and run this script again."
    read -p "Press enter to continue"
    exit
fi

# ask if the user has git installed
read -p "Do you have git and wget installed? (y/n) " gitwget

if [ "$gitwget" = "y" ]; then
    echo "Setting up environment"
else
    echo "Please install git and wget before running this script."
    read -p "Press enter to continue"
    exit
fi

# ask for exllamav2 version
read -p "Want to build stable or dev version of exllamav2? (stable, dev): " exllamav2_version
if [ "$exllamav2_version" != "stable" ] && [ "$exllamav2_version" != "dev" ]; then
    echo "Invalid version of exllama. Please enter stable or dev."
    read -p "Press enter to continue"
    exit
fi

# if CUDA version 12 install pytorch for 12.1, else if CUDA 11 install pytorch for 11.8. If ROCm, install pytorch for ROCm 5.7
read -p "Please enter your GPU compute version, CUDA 11/12 or AMD ROCm (11, 12, rocm): " pytorch_version

if [ "$pytorch_version" = "11" ]; then
    echo "Installing PyTorch for CUDA 11.8"
    venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cu118 --upgrade
elif [ "$pytorch_version" = "12" ]; then
    echo "Installing PyTorch for CUDA 12.1"
    venv/bin/python -m pip install torch
elif [ "$pytorch_version" = "rocm" ]; then
    echo "Installing PyTorch for AMD ROCm 5.7"
    venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/rocm5.7 --upgrade
else
    echo "Invalid compute version. Please enter 11, 12, or rocm."
    read -p "Press enter to continue"
    exit
fi

echo "Deleting potential conflicting files"
rm convert-to-safetensors.py
rm download-model.py
rm -rf exllamav2
rm start-quant.sh
rm enter-venv.sh

# download stuff
echo "Downloading files"
if [ "$exllamav2_version" = "stable" ]; then
    git clone https://github.com/turboderp/exllamav2
elif [ "$exllamav2_version" = "dev" ]; then
    git clone https://github.com/turboderp/exllamav2 -b dev
fi
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/convert-to-safetensors.py
wget https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/download-model.py

echo "Installing pip packages"

venv/bin/python -m pip install -r exllamav2/requirements.txt
venv/bin/python -m pip install huggingface-hub transformers accelerate
venv/bin/python -m pip install ./exllamav2

# create start-quant.sh
echo "#!/bin/bash" > start-quant.sh
echo "venv/bin/python exl2-quant.py" >> start-quant.sh
echo "read -p \"Press enter to continue\"" >> start-quant.sh
echo "exit" >> start-quant.sh
chmod +x start-quant.sh

# create enter-venv.sh
echo "#!/bin/bash" > enter-venv.sh
echo "bash --init-file venv/bin/activate" >> enter-venv.sh
chmod +x enter-venv.sh

echo "If you use ctrl+c to stop, you may need to also use 'pkill python' to stop running scripts."
echo "Environment setup complete. run start-quant.sh to start the quantization process."
read -p "Press enter to exit"
exit