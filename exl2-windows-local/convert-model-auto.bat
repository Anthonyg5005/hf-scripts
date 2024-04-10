@echo off

set /p "model=Folder name: "
set /p "bpw=Target BPW: "
mkdir %model%-exl2-%bpw%bpw
mkdir %model%-exl2-%bpw%bpw-WD
copy %model%\config.json %model%-exl2-%bpw%bpw-WD
venv\scripts\python.exe convert.py -i %model% -o %model%-exl2-%bpw%bpw-WD -cf %model%-exl2-%bpw%bpw -b %bpw%