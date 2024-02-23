#import required functions
from huggingface_hub import login, get_token, whoami
import os

#get token
if os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None: #check if user in kaggle
    from kaggle_secrets import UserSecretsClient
    if UserSecretsClient().get_secret("HF_TOKEN") is not None: #login if token secret found
        login(UserSecretsClient().get_secret("HF_TOKEN"))
    else: #if not found, display instructions and show ipynb login
        print('''
            When using Kaggle, make sure to use the secret key HF_TOKEN with a 'WRITE' token.
            This will prevent the need to login every time you run the script.
            Set your secrets with the secrets add-on on the top of the screen.
             ''')
        notebook_login(write_permission=True)
elif os.environ.get('COLAB_BACKEND_VERSION', None) is not None: #else check if user is in colab
    if get_token() is None: #if token secret not found, display ipynb login
        notebook_login(write_permission=True)
if get_token() is not None:
    #if the token is found then log in:
    login(get_token())
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: "))

#if the token is read only then prompt user to provide a write token (Only required if user needs a WRITE token, remove if READ is enough):
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        if os.environ.get('HF_TOKEN', None) is not None: #if environ finds HF_TOKEN as write then display following text and exit:
            print(f'''
          You have the environment variable HF_TOKEN set.
          You cannot log in.
          Either set the environment variable to a (WRITE) token or remove it.
          ''')
            input("Press enter to continue.")
            exit()
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        login(input("Enter your HuggingFace (WRITE) token: "))
        continue
    break
    