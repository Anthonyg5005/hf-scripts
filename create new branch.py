#import required modules
import os
import huggingface_hub
from huggingface_hub import create_branch

#get user variables
repo = input("Repository name: ")
r_type = input("Repo type (model) (dataset) (space): ")
branch = input("New branch name: ")

#get token
if 'HF_TOKEN' in os.environ:
    #if the variable is found then write it to hf_token:
    hf_token = os.environ['HF_TOKEN']
else:
    #if the variable is not found then prompt user to provide it:
    hf_token = input("HF_TOKEN Variable not detected. Enter your HuggingFace token: ")

#login
huggingface_hub.login(hf_token)

#create the branch
create_branch(repo, repo_type=r_type, branch=branch)
