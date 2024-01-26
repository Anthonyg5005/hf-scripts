#import required modules
import os
import huggingface_hub
from huggingface_hub import create_branch, delete_branch

#set clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#clear screen before starting
clear_screen()

#TODO: get directory and anything else that's needed






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
huggingface_hub.login(hf_token)