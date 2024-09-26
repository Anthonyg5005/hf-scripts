#usually it's what is on the inside that counts, not this time. This script is a mess, but at least it works.
#import required modules
from huggingface_hub import login, get_token, whoami, repo_exists, file_exists, upload_folder, create_repo, upload_file, create_branch, update_repo_visibility
import os
import sys
import subprocess
import glob

#define os differences
oname = os.name
if oname == 'nt':
    osclear = 'cls'
    osmv = 'move'
    osrmd = 'rmdir /s /q'
    oscp = 'copy'
    pyt = 'venv\\scripts\\python.exe'
    slsh = '\\'
elif oname == 'posix':
    osclear = 'clear'
    osmv = 'mv'
    osrmd = 'rm -rf'
    oscp = 'cp'
    pyt = './venv/bin/python'
    slsh = '/'
else:
    sys.exit('This script is not compatible with your machine.')
def clear_screen():
    os.system(osclear)

#get token
if os.environ.get('HF_TOKEN', None) is not None:
    try:
        login(get_token())
    except ValueError:
        print("You have an invalid token set in your environment variable HF_TOKEN. This will cause issues with this script\nRemove the variable or set it to a valid WRITE token.")
        sys.exit("Exiting...")
if os.environ.get('KAGGLE_KERNEL_RUN_TYPE', None) is not None: #check if user in kaggle
    from kaggle_secrets import UserSecretsClient # type: ignore
    from kaggle_web_client import BackendError # type: ignore
    try:
        login(UserSecretsClient().get_secret("HF_TOKEN")) #login if token secret found
    except BackendError: 
        print('''
            When using Kaggle, make sure to use the secret key HF_TOKEN with a 'WRITE' token.
                   This will prevent the need to login every time you run the script.
                   Set your secrets with the secrets add-on on the top of the screen.
             ''')
if get_token() is not None:
    tfound = 'true'
    #if the token is found in either HF_TOKEN or cli login then log in:
    try:
        login(get_token())
    except ValueError:
        login(input("API token is no longer valid. Enter your new HuggingFace (WRITE) token: "))
        tfound = 'false'
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
            You have the environment variable HF_TOKEN set to a 'READ' token.
                                 You cannot log in.
          Either set the environment variable to a 'WRITE' token or remove it.
                  ''')
            input("Press enter to continue.")
            sys.exit("Exiting...")
        if os.environ.get('COLAB_BACKEND_VERSION', None) is not None:
            print('''
                              Your Colab secret key is read-only
                Please switch your key to 'write' or disable notebook access on the left.
                  ''')
            sys.exit("Stuck in loop, exiting...")
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

#get original model repo url
repo_url = input("Enter unquantized model repository (User/Repo): ")

#look for repo
if repo_exists(repo_url) == False:
    print(f"Model repo doesn't exist at https://huggingface.co/{repo_url}")
    sys.exit("Exiting...")
model = repo_url.replace("/", "_")
modelname = repo_url.split("/")[1]
clear_screen()

#ask for number of quants
qmount = int(input("Enter the number of quants you want to create: "))
qmount += 1
clear_screen()

#save bpw values
print(f"Type the BPW for the following {qmount - 1} quants. Recommend staying over 2.4 BPW. Use the vram calculator to find the best BPW values: https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator")
qnum = {}
for i in range(1, qmount):
    qnum[f"bpw{i}"] = float(input(f"Enter BPW for quant {i} (2.00-8.00): ")) #convert input to float for proper sorting
clear_screen()

#collect all values in a list for sorting
bpwvalue = list(qnum.values())

#sort the list from smallest to largest
bpwvalue.sort()

#ask to change repo visibility to public on hf hub
priv2pub = input("Do you want to make the repo public after successful quants? (y/n): ")
while priv2pub != 'y' and priv2pub != 'n':
    priv2pub = input("Please enter 'y' or 'n': ")
clear_screen()

#ask to delete original fp16 weights
delmodel = input("Do you want to delete the original model? (Won't delete if paused or failed) (y/N): ")
if delmodel == '':
    delmodel = 'n'
while delmodel != 'y' and delmodel != 'n':
    delmodel = input("Please enter 'y' or 'n': ")
    if delmodel == '':
        delmodel = 'n'
clear_screen()

#downloading the model
if not os.path.exists(f"models{slsh}{model}{slsh}converted-st"): #check if model was converted to safetensors, skip download if it was
    result = subprocess.run(f"{pyt} download-model.py {repo_url}", shell=True) #download model from hf (Credit to oobabooga for this script)
    if result.returncode != 0:
        print("Download failed.")
        sys.exit("Exiting...")
    clear_screen()

#convert to safetensors if bin
if not glob.glob(f"models/{model}/*.safetensors"): #check if safetensors model exists
    convertst = input("Couldn't find safetensors model, do you want to convert to safetensors? (y/n): ")
    while convertst != 'y' and convertst != 'n':
        convertst = input("Please enter 'y' or 'n': ")
    if convertst == 'y':
        print("Converting weights to safetensors, please wait...")
        result = subprocess.run(f"{pyt} convert-to-safetensors.py models{slsh}{model} --output models{slsh}{model}-st", shell=True) #convert to safetensors (Credit to oobabooga for this script as well)
        if result.returncode != 0:
            print("Converting failed. Please look for a safetensors model or convert model manually.")
            sys.exit("Exiting...")
        subprocess.run(f"{osrmd} models{slsh}{model}", shell=True) #remove previous weights
        subprocess.run(f"{osmv} models{slsh}{model}-st models{slsh}{model}", shell=True) #replace with safetensors
        open(f"models{slsh}{model}{slsh}converted-st", 'w').close()
        print("Finished converting")
    else:
        sys.exit("Can't quantize a non-safetensors model. Exiting...")
clear_screen()

#create new repo if one doesn't already exist
if repo_exists(f"{whoami().get('name', None)}/{modelname}-exl2") == False:
    print("Creating model repository...")
    create_repo(f"{whoami().get('name', None)}/{modelname}-exl2", private=True)
    print(f"Created repo at https://huggingface.co/{whoami().get('name', None)}/{modelname}-exl2") #notify user of repo creation

    #create the markdown file
    print("Writing model card...")
    with open('./README.md', 'w') as file:
        file.write(f"# Exl2 quants for [{modelname}](https://huggingface.co/{repo_url})\n\n")
        file.write("## Automatically quantized using the auto quant script from [hf-scripts](https://huggingface.co/anthonyg5005/hf-scripts)\n\n")
        file.write(f"Would recommend {whoami().get('name', None)} to change up this README to include more info.\n\n")
        file.write("### BPW:\n\n")
        for bpw in bpwvalue:
            file.write(f"[{bpw}](https://huggingface.co/{whoami().get('name', None)}/{modelname}-exl2/tree/{bpw}bpw)\\\n")
        file.write(f"[measurement.json](https://huggingface.co/{whoami().get('name', None)}/{modelname}-exl2/blob/main/measurement.json)\n")
    print("Created README.md")

    upload_file(path_or_fileobj="README.md", path_in_repo="README.md", repo_id=f"{whoami().get('name', None)}/{modelname}-exl2", commit_message="Add temp README") #upload md file
    print("Uploaded README.md to main")
else:
    input("repo already exists, are you resuming a previous process? (Press enter to continue, ctrl+c to exit)")

#start converting
for bpw in bpwvalue:
    if os.path.exists(f"measurements{slsh}{model}-measure{slsh}measurement.json"): # Check if measurement.json exists
        cmdir = False
        mskip = f" -m measurements{slsh}{model}-measure{slsh}measurement.json" #skip measurement if it exists
    else:
        cmdir = True
        mskip = ""
    print(f"Starting quantization for BPW {bpw}")
    os.makedirs(f"{model}-exl2-{bpw}bpw-WD", exist_ok=True) #create working directory
    os.makedirs(f"{model}-exl2-{bpw}bpw", exist_ok=True) #create compile full directory
    subprocess.run(f"{oscp} models{slsh}{model}{slsh}config.json {model}-exl2-{bpw}bpw-WD", shell=True) #copy config to working directory
    #more settings exist in the convert.py script, to veiw them go to docs/convert.md or https://github.com/turboderp/exllamav2/blob/master/doc/convert.md
    result = subprocess.run(f"{pyt} exllamav2/convert.py -i models/{model} -o {model}-exl2-{bpw}bpw-WD -cf {model}-exl2-{bpw}bpw -b {bpw}{mskip} -hb 8 -fst", shell=True) #run quantization and exit if failed (Credit to turbo for his dedication to exl2)
    if result.returncode != 0:
        print("Quantization failed.")
        sys.exit("Exiting...")
    if cmdir == True:
        os.makedirs(f"measurements{slsh}{model}-measure", exist_ok=True) #create measurement directory
        subprocess.run(f"{oscp} {model}-exl2-{bpw}bpw-WD{slsh}measurement.json measurements{slsh}{model}-measure", shell=True) #copy measurement to measure directory
        open(f"measurements{slsh}{model}-measure/Delete folder when no more quants are needed from this model", 'w').close()
    try:
        create_branch(f"{whoami().get('name', None)}/{modelname}-exl2", branch=f"{bpw}bpw") #create branch
    except:
        print(f"Branch {bpw} already exists, trying upload...")
    upload_folder(folder_path=f"{model}-exl2-{bpw}bpw", repo_id=f"{whoami().get('name', None)}/{modelname}-exl2", commit_message=f"Add quant for BPW {bpw}", revision=f"{bpw}bpw") #upload quantized model
    subprocess.run(f"{osrmd} {model}-exl2-{bpw}bpw-WD", shell=True) #remove working directory
    subprocess.run(f"{osrmd} {model}-exl2-{bpw}bpw", shell=True) #remove compile directory

if file_exists(f"{whoami().get('name', None)}/{modelname}-exl2", "measurement.json") == False: #check if measurement.json exists in main
    upload_file(path_or_fileobj=f"measurements{slsh}{model}-measure{slsh}measurement.json", path_in_repo="measurement.json", repo_id=f"{whoami().get('name', None)}/{modelname}-exl2", commit_message="Add measurement.json") #upload measurement.json to main

# if chose to delete model at the beginning, delete the model
if delmodel == 'y':
    subprocess.run(f"{osrmd} models{slsh}{model}", shell=True)
    print(f"Deleted models/{model}")

#update repo visibility if user chose to
if priv2pub == 'y':
    update_repo_visibility(f"{whoami().get('name', None)}/{modelname}-exl2", private=False)
    print("Repo is now public.")

#if new sign in, tell user
if tfound == 'false':
    print(f'''
              You are now logged in as {whoami().get('fullname', None)}.
          
          To logout, use the hf command line interface 'huggingface-cli logout'
               To view your active account, use 'huggingface-cli whoami'
          ''')
    
print(f'''Quants available at https://huggingface.co/{whoami().get('name', None)}/{modelname}-exl2''')