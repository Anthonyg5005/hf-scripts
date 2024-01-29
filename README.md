---
license: unlicense
---
# scripts

Personal scripts to automate some tasks.\
Will try to keep external module use to a minimum, other than **huggingface_hub**.\
Feel free to send in pull requests or use this code however you'd like.

**For Github**: Would recommend creating pull requests and discussions on the [offical huggingface repo](https://huggingface.co/Anthonyg5005/hf-scripts)

## existing scripts

- [Manage branches (create/delete)](https://huggingface.co/Anthonyg5005/hf-scripts/blob/main/manage%20branches.py)

## work in progress/not tested ([unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch)

- Push to hf hub

## other recommended scripts

- [Download models (download HF Hub models) [Oobabooga]](https://github.com/oobabooga/text-generation-webui/blob/main/download-model.py)

## usage

- Manage branches
  - Run script and follow prompts. You will be required to be logged in to HF Hub. If you are not logged in, you will need a WRITE token. You can get one in your [HuggingFace settings](https://huggingface.co/settings/tokens). May get some updates in the future for handling more situations. All active updates will be on the [unfinished](https://huggingface.co/Anthonyg5005/hf-scripts/tree/unfinished) branch.
  
- Download models
  - Make sure you have [requests](https://pypi.org/project/requests/) and [tqdm](https://pypi.org/project/tqdm/) installed. You can install them with "`pip install requests tqdm`". To use the script, open a terminal and run "`python download-model.py USER/MODEL:BRANCH`". There's also a "`--help`" flag to show the available arguments. To download from private repositories, HF_TOKEN variable needs to be set to at least a READ token ([Dev](https://github.com/oobabooga/text-generation-webui/blob/dev/download-model.py) branch can use cli login).
