#import required modules
import os
from huggingface_hub import create_branch, push_to_hub, login, get_token, whoami

#define clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#clear screen before starting
clear_screen()

#store actions into variables
#TODO change to whatever is needed or delete
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
    tfound = "bruh"
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

#TODO prompt the user for confirmation on upload
while True:
    yorn = input(f"Are you sure you want to REPLACE WITH ACTION (Y/n): ").lower()
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

#TODO upload the files

#extra information for the user
#if token wasn't found from line 36 then display following text:
if tfound == 'false':
    print(f'''
          You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
          To view your active account, use 'huggingface-cli whoami'
          ''')
input("Press enter to continue.")
