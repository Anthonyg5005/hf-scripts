---
license: unlicense
language:
- en
---
# scripts

Personal scripts to automate some tasks.\
Will try to keep external module use to a minimum, other than **huggingface_hub**.\
Feel free to send in PRs or use this code however you'd like.\
*[GitHub mirror](https://github.com/anthonyg5005/hf-scripts)*

**For GitHub**: Would recommend creating pull requests and discussions on the [offical huggingface repo](https://huggingface.co/Anthonyg5005/hf-scripts)

## existing files

- [Manage branches (create/delete)](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/manage%20branches.py)

- [EXL2 Private Quant V3](https://colab.research.google.com/drive/1Vc7d6JU3Z35OVHmtuMuhT830THJnzNfS?usp=sharing) **(COLAB)**

- [Upload folder to repo](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/upload%20folder%20to%20repo.py)

## work in progress/not tested ([unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch)

- Auto exl2 upload script
  - Will create repo and create 5 custom quants on individual branches
  - Windows/Linux support

## other recommended stuff

- [Exllama Discord server](https://discord.gg/NSFwVuCjRq) Free Exl2 quantizing bot by the Bloke and Lambda Labs available.
  - existing quants under the HF account [@blockblockblock](https://huggingface.co/blockblockblock)

- [Download models (download HF Hub models) [Oobabooga]](https://github.com/oobabooga/text-generation-webui/blob/main/download-model.py)

## usage

- Manage branches
  - Run script and follow prompts. You will be required to be logged in to HF Hub. If you are not logged in, you will need a WRITE token. You can get one in your [HuggingFace settings](https://huggingface.co/settings/tokens). May get some updates in the future for handling more situations. All active updates will be on the [unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch. Colab and Kaggle keys are supported.

- EXL2 Private Quant
  - Allows you to quantize to exl2 using colab. This version creates a exl2 quant to upload to private repo. Should work on any Linux jupyterlab server with CUDA, ROCM should be supported by exl2 but not tested.
 
- Upload folder to repo
  - Uploads user specified folder to specified repo, can create private repos too. Not the same as git commit and push, instead uploads any additional files.
  
- Download models
  - Make sure you have [huggingface_hub](https://pypi.org/project/huggingface-hub/) installed as it has the same dependencies. You can install it with '`pip install huggingface-hub`'. To use the script, open a terminal and run '`python download-model.py USER/MODEL:BRANCH`'. There's also a '`--help`' flag to show the available arguments. To download from private repositories, make sure to login using '`huggingface-cli login`' or (not recommended) `HF_TOKEN` environment variable.

## extras

- [HF login snippet](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet.py)
  - The login method that I wrote to make fetching the token better.
- [HF login snippet kaggle](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/HF%20Login%20Snippet%20Kaggle.py)
  - Same as above but for cloud ipynb environments like Colab and Kaggle (Kaggle secret support)
