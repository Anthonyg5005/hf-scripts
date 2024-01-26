#import required modules
import os
import huggingface_hub
from huggingface_hub import create_branch

#get user variables
repo = input("Repository name: ")
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space']:
        print("Please choose one of the three options.")
        continue
    
    break
branch = input("New branch name (No spaces): ")

#get token
if 'HF_TOKEN' in os.environ:
    #if the variable is found then write it to hf_token:
    hf_token = os.environ['HF_TOKEN']
    tfound = "true"
else:
    #if the variable is not found then prompt user to provide it:
    hf_token = input("HF_TOKEN Variable not detected. Enter your HuggingFace (WRITE) token: ")
    tfound = "false"

#login
huggingface_hub.login(hf_token)

#create the branch
create_branch(repo, repo_type=r_type, branch=branch)

#extra information
#won't work if special characters are used
if r_type == 'model':
    print(f"Branch created at https://huggingface/{repo}/tree/{branch}")
elif r_type == 'dataset':
    print(f"Branch created at https://huggingface/datasets/{repo}/tree/{branch}")
elif r_type == 'space':
    print(f"Branch created at https://huggingface/spaces/{repo}/tree/{branch}")
#if token wasn't found then display following text:
if tfound == 'false':
    print('''
          Set HF_TOKEN to a token with WRITE permissions to skip inputting token on each run.
          
          On Unix systems, edit the file ~/.bashrc with an editor of your choise.
          On a new line add: export HF_TOKEN=Your-HuggingFace-token-here
          (Terminal Refresh Required)
          To temporarily set a token to the active terminal use 'export HF_TOKEN=Your-HuggingFace-token-here'
          
          On Windows use 'setx HF_TOKEN Your-HuggingFace-token-here'
          (System Restart Required)
          To temporarily set a token to the active terminal use 'set HF_TOKEN=Your-HuggingFace-token-here'
          ''')
input("Press enter to continue.")
