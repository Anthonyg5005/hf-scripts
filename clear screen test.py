import os
#set clear screen variable
clrscr = os.system('cls' if os.name == 'nt' else 'clear')

#get user variables
while True:
    cord = input("What would you like to do? (create) (delete): ").lower()
    
    if cord not in ['create', 'delete']:
        print("Please choose one of the two options.")
        continue
    
    break
clrscr
repo = input("Repository name: ")
clrscr
while True:
    r_type = input("Repo type (model) (dataset) (space): ").lower()
    
    if r_type not in ['model', 'dataset', 'space']:
        print("Please choose one of the three options.")
        continue
    
    break
clrscr
branch = input("New branch name (No spaces): ")
clrscr