---
license: unlicense
language:
- en
---
# scripts

Personal scripts to automate some tasks.\
Most of this is to get me familiar with python and hf_hub.\
Will try to keep external module use to a minimum, other than **huggingface_hub**.\
Feel free to send in pull requests or use this code however you'd like.\
*[GitHub mirror](https://github.com/anthonyg5005/hf-scripts)*

**For GitHub**: Would recommend creating pull requests and discussions on the [offical huggingface repo](https://huggingface.co/Anthonyg5005/hf-scripts)

## existing files

- [Manage branches (create/delete)](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/manage%20branches.py)

- [EXL2 Private Quant V2](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/EXL2_Private_Quant_V2.ipynb) **(COLAB)** testing, will potentially be available within two hours of this update, in files for now.

## work in progress/not tested ([unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch)

- EXL2 Private Quant V3
  - Allow for converting jsonl to parquet and bin to safetensors

- Auto exl2 upload ipynb
  - Will create repo and have quants from 2-6 bpw (or custom) on individual branches
  - Also batch/bash scripts afterwards for non jupyterlab environments

- Upload folder
  - Will allow to upload a folder to existing or new repo

## other recommended files

- [Download models (download HF Hub models) [Oobabooga]](https://github.com/oobabooga/text-generation-webui/blob/main/download-model.py)

## usage

- Manage branches
  - Run script and follow prompts. You will be required to be logged in to HF Hub. If you are not logged in, you will need a WRITE token. You can get one in your [HuggingFace settings](https://huggingface.co/settings/tokens). May get some updates in the future for handling more situations. All active updates will be on the [unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch. Colab and Kaggle keys are supported.

- EXL2 Private Quant
  - Allows you to quantize to exl2 using colab. This version creates a exl2 quant to upload to private repo. Should work on any Linux jupyterlab server with CUDA, ROCM should be supported by exl2 but not tested. Currently being built to later on become the base of `'Auto exl2 upload ipynb'`.
  
- Download models
  - Make sure you have [requests](https://pypi.org/project/requests/) and [tqdm](https://pypi.org/project/tqdm/) installed. You can install them with '`pip install requests tqdm`'. To use the script, open a terminal and run '`python download-model.py USER/MODEL:BRANCH`'. There's also a '`--help`' flag to show the available arguments. To download from private repositories, make sure to login using '`huggingface-cli login`' or (not recommended) `HF_TOKEN` environment variable.

## extras

- [HF login snippet](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet.py)
  - The login method that I wrote to make fetching the token better.
- [HF login snippet kaggle](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet%20Kaggle.py)
  - Same as above but for cloud ipynb environments like Colab and Kaggle (Kaggle secret support)
