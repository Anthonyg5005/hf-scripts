#import required functions
from huggingface_hub import login, get_token, whoami

#define clear screen function (OPTIONAL)
oname = os.name
if oname == 'nt':
    osclear = 'cls'
elif oname == 'posix':
    osclear = 'clear'
else:
    osclear = ''
def clear_screen():
    os.system(osclear)

#get token
if get_token() is not None:
    #if the token is found in either HF_TOKEN or cli login then log in:
    login(get_token())
    tfound = 'true' #remove if lines 27-34 removed
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: ")) # can remove "(WRITE)" if not required
    tfound = 'false' #remove if lines 27-34 removed

#if the token is read only then prompt user to provide a write token (Only required if user needs a WRITE token, remove if READ is enough):
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        clear_screen()
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

#if token wasn't found at first then print the name of the new logged in user (OPTIONAL)
if tfound == 'false':
    print(f'''
          You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
          To view your active account, use 'huggingface-cli whoami'
          ''')
    