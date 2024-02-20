#import required modules
import os
from huggingface_hub import create_branch, delete_branch, login, get_token, whoami

#define clear screen function
if os.name == 'nt':
    osclear = 'cls'
elif os.name == 'posix':
    osclear = 'clear'
else:
    osclear = ''
def clear_screen():
    os.system(osclear)

#clear screen before starting
clear_screen()

#store actions into variables
#create or delete (restricted)
while True:
    cord = input("What would you like to do? (create) (delete): ").lower()
    
    if cord not in ['create', 'delete', 'c', 'd']:
        clear_screen()
        print("Please choose one of the following two options.")
        continue
    if cord == 'c':
        cord = 'create'
    elif cord == 'd':
        cord = 'delete'
    break
clear_screen()
#name of affected repository
repo = input("Repository name (User/Repo): ")
clear_screen()
#type of huggingface repository (restricted)
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space', 'm', 'd', 's']:
        clear_screen()
        print("Please choose one of the following three options.")
        continue
    if r_type == 'm':
        r_type = 'model'
    elif r_type == 'd':
        r_type = 'dataset'
    elif r_type == 's':
        r_type = 'space'
    break
clear_screen()
#name of created or deleted branch
branch = input("Branch name (No spaces): ")
clear_screen()
#promt user for revision, or clone from main
if cord == 'create':
    rev = input("Revision to clone from (Can be a branch name or the OID/SHA of a commit) (Empty clones main): ")
    if rev == '':
        rev = 'main'
clear_screen()

#get token
if get_token() is not None:
    #if the token is found then log in:
    login(get_token())
    tfound = "Where are my doritos?"
else:
    if os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None: #check if user in kaggle
        print('''
              When using Kaggle, make sure to use the secret key HF_TOKEN with a 'WRITE' token.
              This will prevent the need to login every time you run the script.
              Set your secrets with the secrets add-on on the top of the screen.
              ''')
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: "))
    tfound = "false"

#if the token is read only then prompt user to provide a write token:
envariable = 'false for now'
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        if os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None: #check if user in kaggle
            print('''
                  When using Kaggle, make sure to use the secret key HF_TOKEN with a 'WRITE' token.
                  This will prevent the need to login every time you run the script.
                  Set your secrets with the secrets add-on on the top of the screen.
                  ''')
        clear_screen()
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        login(input("Enter your HuggingFace (WRITE) token: "))
        if os.environ.get('HF_TOKEN', None) is not None:
            envariable = 'true'
        continue
    break

clear_screen()
if cord == 'delete':
    #prompt the user for confirmation on deletion of the branch
    while True:
        yorn = input(f"Are you sure you want to remove branch '{branch}' in {repo}? (Y/n): ").lower()
        if yorn == '':
            yorn = 'y'
            break
        else:
            if yorn not in ['y', 'n']:
                clear_screen()
                print("Please choose one of the following two options carefully.")
                continue
        break
else:
    #prompt the user for confirmation on creation of the branch
    while True:
        yorn = input(f"Are you sure you want to clone revision '{rev}' to create branch '{branch}' in {repo}? (Y/n): ").lower()
        if yorn == '':
            yorn = 'y'
        elif yorn == 'yes':
            yorn = 'y'
        elif yorn == 'no':
            yorn = 'n'
            break
        else:
            if yorn not in ['y', 'n']:
                clear_screen()
                print("Please choose one of the following two options carefully.")
                continue
        break
clear_screen()

#create or delete the branch
#if user selected yes then continue, else exit
if yorn == 'y':
    if cord == 'create':
        create_branch(repo, revision=rev, repo_type=r_type, branch=branch)
    else:
        delete_branch(repo, repo_type=r_type, branch=branch)
else:
    print("Cancelled action")
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
#if token wasn't found from line 60 then display following text:
if tfound == 'false':
    print(f'''
          You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
          To view your active account, use 'huggingface-cli whoami'
          ''')

#if environ finds HF_TOKEN then display following text:
if envariable == 'true':
    print(f'''
          You have the environment variable HF_TOKEN set.
          This may interfere with the huggingface login every time script is ran.
          ''')
input("Press enter to continue.")
