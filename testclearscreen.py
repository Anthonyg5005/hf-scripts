#import required modules
import os
import huggingface_hub
from huggingface_hub import create_branch, delete_branch

#set clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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