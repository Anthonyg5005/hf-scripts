---
license: agpl-3.0
language:
- en
---
# scripts

Personal scripts to automate some tasks.\
Will try to keep external module use to a minimum, other than **huggingface_hub**.\
Feel free to send in PRs or use this code however you'd like. External downloaded code after running are AGPL 3.0 but anything I write is unlicense.\
*[GitHub mirror](https://github.com/anthonyg5005/hf-scripts)*

**For GitHub**: Would recommend creating pull requests and discussions on the [offical huggingface repo](https://huggingface.co/Anthonyg5005/hf-scripts)

## existing files

- [Auto EXL2 HF upload](https://huggingface.co/Anthonyg5005/hf-scripts/resolve/main/auto-exl2-upload/auto-exl2-upload.zip?download=true)

- [EXL2 Local Quants](https://huggingface.co/Anthonyg5005/hf-scripts/resolve/main/exl2-multi-quant-local/exl2-multi-quant-local.zip?download=true)

- [Upload folder to HF](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/upload%20folder%20to%20repo.py)

- [Manage branches (create/delete)](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/manage%20branches.py)

- [EXL2 Single Quant V3](https://colab.research.google.com/drive/1Vc7d6JU3Z35OVHmtuMuhT830THJnzNfS?usp=sharing) **(COLAB)**

## work in progress/not tested ([unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch)

- Seems I've got nothing to work on right now

## other recommended stuff

- [Exllama Discord server](https://discord.gg/NSFwVuCjRq) Free Exl2 quantizing bot sponsored by The Bloke and Lambda Labs, managed by Kaltcit.
  - existing quants under the HF account [@blockblockblock](https://huggingface.co/blockblockblock)

- [Download models (download HF Hub models) [Oobabooga]](https://github.com/oobabooga/text-generation-webui/blob/main/download-model.py)

## usage

- Auto EXL2 HF upload
  - This script is designed to automate the process of quantizing models to EXL2 and uploading them to the HF Hub as seperate branches. This is both available to run on Windows and Linux. You will be required to be logged in to HF Hub. If you are not logged in, you will need a WRITE token.
  - [Example repo](https://huggingface.co/Anthonyg5005/Qwen1.5-0.5B-Chat-exl2)

- EXL2 Local Quants
  - Easily creates environment to quantize models to exl2 to your local machine. Supports both Windows and Linux.

- Upload folder to repo
  - Uploads user specified folder to specified repo, can create private repos too. Not the same as git commit and push, instead uploads any additional files. This is more to be modified to your needs then used by itself.

- Manage branches
  - Run script and follow prompts. You will be required to be logged in to HF Hub. If you are not logged in, you will need a WRITE token. You can get one in your [HuggingFace settings](https://huggingface.co/settings/tokens). Colab and Kaggle secret keys are supported.

- EXL2 Single Quant
  - Allows you to quantize to exl2 using colab. This version creates a exl2 quant to upload to private repo. Only 7B tested on colab.
  
- Download models
  - To use the script, open a terminal and run '`python download-model.py USER/MODEL:BRANCH`'. There's also a '`--help`' flag to show the available arguments. To download from private repositories, make sure to login using '`huggingface-cli login`' or (not recommended) `HF_TOKEN` environment variable.

## extras

- [HF login snippet](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet.py)
  - The login method that I wrote to make fetching the token better.
- [HF login snippet kaggle](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet%20Kaggle.py)
  - Same as above but for cloud ipynb environments like Colab and Kaggle (Kaggle secret support)
