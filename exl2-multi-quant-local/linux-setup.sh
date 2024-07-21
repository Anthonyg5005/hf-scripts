#!/bin/bash

# converted from windows-setup.bat by github copilot

# check if "venv" subdirectory exists, if not, create one
if [ ! -d "venv" ]; then
    python -m venv venv
else
    read -p "venv directory already exists. Looking to upgrade/reinstall exllama? (will reinstall python venv) (y/n) " reinst
    if [ "$reinst" = "y" ]; then
        rm -rf venv
        python -m venv venv
    else
        exit
    fi
fi

# ask if the user has git installed
read -p "Do you have git and wget installed? (y/n) " gitwget

if [ "$gitwget" = "y" ]; then
    echo "Setting up environment"
else
    echo "Please install git and wget from your distro's package manager before running this script."
    echo "Example for Debian-based: sudo apt-get install git wget"
    echo "Example for Arch-based: sudo pacman -S git wget"
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

# ask to install flash attention
echo "Flash attention is a feature that could fix overflow issues on some more broken models, however, it will increase install time by a few hours."
read -p "Would you like to install flash-attention? (rarely needed and optional) (y/n) " flash_attention
if [ "$flash_attention" != "y" ] && [ "$flash_attention" != "n" ]; then
    echo "Invalid input. Please enter y or n."
    read -p "Press enter to continue"
    exit
fi

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

echo "Writing shell files..."

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

if [ "$flash_attention" = "y" ]; then
    echo "Going to attempt to install flash attention but it isn't required."
    echo "You may close now if you'd like and continue without flash attention."
    read -p "Press enter to continue and install flash attention"
    echo "Get some popcorn and watch a movie, this will take a while."
    echo "Installing flash-attn..."
    venv/bin/python -m pip install git+https://github.com/Dao-AILab/flash-attention.git
fi

echo "If you use ctrl+c to stop, you may need to also use 'pkill python' to stop running scripts."
echo "Environment setup complete. run start-quant.sh to start the quantization process."
read -p "Press enter to exit"
exit
