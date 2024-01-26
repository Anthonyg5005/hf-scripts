#import required modules
import os
from huggingface_hub import create_branch, delete_branch, login, get_token

#set clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#clear screen before starting
clear_screen()

#get user variables
while True:
    cord = input("What would you like to do? (create) (delete): ").lower()
    
    if cord not in ['create', 'delete']:
        clear_screen()
        print("Please choose one of the two options.")
        continue
    break
clear_screen()
repo = input("Repository name: ")
clear_screen()
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space']:
        clear_screen()
        print("Please choose one of the three options.")
        continue
    break
clear_screen()
branch = input("New branch name (No spaces): ")
clear_screen()

#get token
if 'HF_TOKEN' in os.environ:
    #if the variable is found then write it to hf_token:
    hf_token = os.environ['HF_TOKEN']
    tfound = "Where are my doritos?"
else:
    #if the variable is not found then prompt user to provide it:
    hf_token = input("HF_TOKEN Variable not detected. Enter your HuggingFace (WRITE) token: ")
    tfound = "false"

#login
login(hf_token)

#create or delete the branch
if cord == 'create':
    create_branch(repo, repo_type=r_type, branch=branch)
else:
    delete_branch(repo, repo_type=r_type, branch=branch)

#extra information
clear_screen()
#won't work if special characters are used but should still successfully be created/deleted
if cord == 'create':
    if r_type == 'model':
        print(f"Branch created at https://huggingface.co/{repo}/tree/{branch}")
    elif r_type == 'dataset':
        print(f"Branch created at https://huggingface.co/datasets/{repo}/tree/{branch}")
    elif r_type == 'space':
        print(f"Branch created at https://huggingface.co/spaces/{repo}/tree/{branch}")
else:
    if r_type == 'model':
        print(f"Branch deleted on {r_type} https://huggingface.co/{repo}")
    elif r_type == 'dataset':
        print(f"Branch deleted on {r_type} https://huggingface.co/datasets/{repo}")
    elif r_type == 'space':
        print(f"Branch deleted on {r_type} https://huggingface.co/spaces/{repo}")
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
