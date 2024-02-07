#import required functions
from huggingface_hub import login, get_token

#define clear screen function (not required but remove the function from code if this is removed)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#get token
if get_token() is not None:
    #if the token is found in either HF_TOKEN or cli login then log in:
    login(get_token())
else:
    #if the token is not found then prompt user to provide it:
    login(input("API token not detected. Enter your HuggingFace (WRITE) token: ")) # can remove "(WRITE)" if not required

#if the token is read only then prompt user to provide a write token (Only required if user needs a WRITE token, remove if READ is enough):
while True:
    if whoami().get('auth', {}).get('accessToken', {}).get('role', None) != 'write':
        clear_screen()
        print("You do not have write access to this repository. Please use a valid token with (WRITE) access.")
        login(input("Enter your HuggingFace (WRITE) token: "))
        continue
    break
