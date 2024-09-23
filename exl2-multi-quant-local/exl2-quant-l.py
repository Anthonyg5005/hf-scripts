#usually it's what is on the inside that counts, not this time. This script is a mess, but at least it works.
#import required modules
from huggingface_hub import login, logout, get_token, whoami, repo_exists
import os
import sys
import subprocess
import glob
import time

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

#get original model repo url
repo_url = input("Enter unquantized model repository (User/Repo): ")

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

#ask to delete fp16 after done
delmodel = input("Do you want to delete the original model? (Won't delete if paused or failed) (y/N): ")
if delmodel == '':
    delmodel = 'n'
while delmodel != 'y' and delmodel != 'n':
    delmodel = input("Please enter 'y' or 'n': ")
    if delmodel == '':
        delmodel = 'n'
if delmodel == 'y':
    print(f"Deleting dir models/{model} after quants are finished.")
    time.sleep(3)
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
    os.makedirs(f"{modelname}-exl2-quants{slsh}{modelname}-exl2-{bpw}bpw", exist_ok=True) #create compile full directory
    subprocess.run(f"{oscp} models{slsh}{model}{slsh}config.json {model}-exl2-{bpw}bpw-WD", shell=True) #copy config to working directory
    #more settings exist in the convert.py script, to veiw them go to docs/convert.md or https://github.com/turboderp/exllamav2/blob/master/doc/convert.md
    result = subprocess.run(f"{pyt} exllamav2/convert.py -i models/{model} -o {model}-exl2-{bpw}bpw-WD -cf {modelname}-exl2-quants{slsh}{modelname}-exl2-{bpw}bpw -b {bpw}{mskip} -hb 8", shell=True) #run quantization and exit if failed (Credit to turbo for his dedication to exl2)
    if result.returncode != 0:
        print("Quantization failed.")
        sys.exit("Exiting...")
    if cmdir == True:
        os.makedirs(f"measurements{slsh}{model}-measure", exist_ok=True) #create measurement directory
        subprocess.run(f"{oscp} {model}-exl2-{bpw}bpw-WD{slsh}measurement.json measurements{slsh}{model}-measure", shell=True) #copy measurement to measure directory
        open(f"measurements{slsh}{model}-measure/Delete folder when no more quants are needed from this model", 'w').close()
    subprocess.run(f"{osrmd} {model}-exl2-{bpw}bpw-WD", shell=True) #remove working directory
    
# if chose to delete model at the beginning, delete the model
if delmodel == 'y':
    subprocess.run(f"{osrmd} models{slsh}{model}", shell=True)
    print(f"Deleted models/{model}")
    
print("Finished quantizing. Exiting...")
