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

#TODO: verify that the token is WRITE and not READ

if get_token() == 'None':
    #if the token is not found then prompt user to provide it:
    hf_token = input("API token not detected. Enter your HuggingFace (WRITE) token: ")
    tfound = "false"
else:
    #if the token is found then write it to hf_token:
    hf_token = get_token()
    tfound = "Where are my doritos?"

#login
login(hf_token)


#TODO: get fullname from whoami()
uname = ""



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
    print(f'''
          You were logged in as {uname}.
          
          To logout, use the cli 'huggingface-cli logout'
          TO view your active account, use 'huggingface-cli whoami'
          ''')
input("Press enter to continue.")
