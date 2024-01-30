#import required modules
import os
from huggingface_hub import create_branch, delete_branch, login, get_token, whoami

#define clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#clear screen before starting
clear_screen()

#store actions into variables
#create or delete (restricted)
while True:
    cord = input("What would you like to do? (create) (delete): ").lower()
    
    if cord not in ['create', 'delete']:
        clear_screen()
        print("Please choose one of the following two options.")
        continue
    break
clear_screen()
#name of effected repository
repo = input("Repository name (User/Repo): ")
clear_screen()
#type of huggingface repository (restricted)
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space']:
        clear_screen()
        print("Please choose one of the following three options.")
        continue
    break
clear_screen()
#name of created or deleted branch
branch = input("Branch name (No spaces): ")
clear_screen()

#get token
if get_token() is not None:
    #if the token is found then log in:
    login(get_token())
    tfound = "Where are my doritos?"
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: "))
    tfound = "false"

#if the token is read only then prompt user to provide a write token:
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        clear_screen()
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        login(input("Enter your HuggingFace (WRITE) token: "))
        continue
    break

#prompt the user for confirmation on creation/deletion of the branch
while True:
    yorn = input(f"Are you sure you want to {cord} branch '{branch}' in {repo} (Y/n): ").lower()
    if yorn == '':
        yorn = y
        break
    else:
        if yorn not in ['y', 'n']:
            clear_screen()
            print("Please choose one of the following two options carefully.")
            continue
    break
clear_screen()

#create or delete the branch
if yorn == 'y':
    if cord == 'create':
        create_branch(repo, repo_type=r_type, branch=branch)
    else:
        delete_branch(repo, repo_type=r_type, branch=branch)
else:
    exit()
clear_screen()

#extra information for the user
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
#if token wasn't found from line 36 then display following text:
if tfound == 'false':
    print(f'''
          You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
          To view your active account, use 'huggingface-cli whoami'
          ''')
input("Press enter to continue.")
