#import required functions
import os
from huggingface_hub import login, get_token, whoami

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
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: "))

#if the token is read only then prompt user to provide a write token (Only required if user needs a WRITE token, remove if READ is enough):
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
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
    