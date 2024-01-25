import os
import huggingface_hub
from huggingface_hub import create_branch

#get user variables
repo = input("Repository name: ")
branch = input("New branch name: ")

#login
huggingface_hub.login(os.environ['HF_TOKEN'])

#create the branch
create_branch(f"{repo}", repo_type="model", branch=f"{branch}")
