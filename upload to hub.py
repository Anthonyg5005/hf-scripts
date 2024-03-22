#import required functions
import os
from huggingface_hub import login, get_token, whoami, HfApi, create_repo, repo_exists

#define clear screen function
oname = os.name
if oname == 'nt':
    osclear = 'cls'
elif oname == 'posix':
    osclear = 'clear'
else:
    osclear = ''
def clear_screen():
    os.system(osclear)

#clear before starting
clear_screen()

#get token
if os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None: #check if user in kaggle
    from kaggle_secrets import UserSecretsClient
    from kaggle_web_client import BackendError
    try:
        login(UserSecretsClient().get_secret("HF_TOKEN")) #login if token secret found
    except BackendError: 
        print('''
            When using Kaggle, make sure to use the secret key HF_TOKEN with a 'WRITE' token.
                   This will prevent the need to login every time you run the script.
                   Set your secrets with the secrets add-on on the top of the screen.
             ''')
if get_token() is not None:
    #if the token is found then log in:
    login(get_token())
    tfound = "Where are my doritos?" #doesn't matter what this is, only false is used
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: "))
    tfound = "false"

#if the token is read only then prompt user to provide a write token:
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        clear_screen()
        if os.environ.get('HF_TOKEN', None) is not None: #if environ finds HF_TOKEN as read-only then display following text and exit:
            print('''
                  You have the environment variable HF_TOKEN set.
                                 You cannot log in.
          Either set the environment variable to a 'WRITE' token or remove it.
                  ''')
            input("Press enter to continue.")
            exit()
        if os.environ.get('COLAB_BACKEND_VERSION', None) is not None:
            print('''
                              Your Colab secret key is read-only
                Please switch your key to 'write' or disable notebook access on the left.
                               For now, you are stuck in a loop
                  ''')
        elif os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None:
            print('''
                                      Your Kaggle secret key is read-only
                Please switch your key to 'write' or unattach from notebook in add-ons at the top.
                          Having a read-only key attched will require login every time.
                ''')
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        login(input("Enter your HuggingFace (WRITE) token: "))
        continue
    break
clear_screen()

#store actions into variables
#upload directory
up_dir = input("Enter the directory you want to upload: ")
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

#if new, ask for private
priv = "nothing yet"
if repo_exists(repo, repo_type=r_type) == False:
    while True:
        priv = input(f"Create private repository? (y/N): ").lower()
        if priv == '':
            priv = 'n'
        elif priv == 'yes':
            priv = 'y'
        elif priv == 'no':
            priv = 'n'
            break
        else:
            if priv not in ['y', 'n']:
                clear_screen()
                print("Please choose one of the following two options.")
                continue
        break
clear_screen()

c_mes = input("Commit message (optional): ")
if c_mes == "":
    c_mes = "Uploaded folder with huggingface_hub"

#TODO revision support. if branch not automatically created, create before uploading

#upload the folder
if priv == "y":
    create_repo(repo, repo_type=r_type, private=True) #if private chosen, create private repo first
HfApi().upload_folder(folder_path=up_dir, repo_id=repo, repo_type=r_type, commit_message=c_mes)

if r_type == 'model':
    print(f"Repository created at https://huggingface.co/{repo}")
elif r_type == 'dataset':
    print(f"Repository created at https://huggingface.co/datasets/{repo}")
elif r_type == 'space':
    print(f"Repository created at https://huggingface.co/spaces/{repo}")

if tfound == 'false':
    print(f'''
              You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
               To view your active account, use 'huggingface-cli whoami'
          ''')

input("Press enter to continue.")
