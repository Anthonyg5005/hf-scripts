#import required modules
import os
from huggingface_hub import create_branch, delete_branch, login, get_token, whoami

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
        print("Please choose one of the following two options.")
        continue
    break
clear_screen()
repo = input("Repository name (User/Repo): ")
clear_screen()
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space']:
        clear_screen()
        print("Please choose one of the following three options.")
        continue
    break
clear_screen()
branch = input("Branch name (No spaces): ")
clear_screen()

#get token
if 'None' in str(get_token()):
    #if the token is not found then prompt user to provide it:
    hf_token = input("API token not detected. Enter your HuggingFace (WRITE) token: ")
    tfound = "false"
else:
    #if the token is found then write it to hf_token:
    hf_token = get_token()
    tfound = "Where are my doritos?"
#if the token is read only then prompt user to provide a write token:
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        clear_screen()
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        hf_token = input("Enter your HuggingFace (WRITE) token: ")
        continue
    break

#login
login(hf_token)
#store the user's name
fname = whoami().get('fullname', None)

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
        print(f"Branch {branch} created at https://huggingface.co/{repo}/tree/{branch}")
    elif r_type == 'dataset':
        print(f"Branch {branch} created at https://huggingface.co/datasets/{repo}/tree/{branch}")
    elif r_type == 'space':
        print(f"Branch {branch} created at https://huggingface.co/spaces/{repo}/tree/{branch}")
else:
    if r_type == 'model':
        print(f"Branch {branch} deleted on {r_type} https://huggingface.co/{repo}")
    elif r_type == 'dataset':
        print(f"Branch {branch} deleted on {r_type} https://huggingface.co/datasets/{repo}")
    elif r_type == 'space':
        print(f"Branch {branch} deleted on {r_type} https://huggingface.co/spaces/{repo}")
#if token wasn't found then display following text:
if tfound == 'false':
    print(f'''
          You are now logged in as {fname}.
          
          To logout, use the cli 'huggingface-cli logout'
          To view your active account, use 'huggingface-cli whoami'
          ''')
input("Press enter to continue.")
