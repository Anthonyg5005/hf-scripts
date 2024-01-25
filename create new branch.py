import os
import huggingface_hub
from huggingface_hub import create_branch

#get user variables
repo = input("Repository name: ")
r_type = input("Repo type (model) (dataset) (space): ")
branch = input("New branch name: ")

#login
huggingface_hub.login(os.environ['HF_TOKEN'])

#create the branch
create_branch(repo, repo_type=r_type, branch=branch)
