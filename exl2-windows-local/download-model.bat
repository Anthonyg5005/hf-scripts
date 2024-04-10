@echo off

echo Enter the model repo. User/Repo:Branch (Branch optional)
set /p "repo=Model repo: "
venv\scripts\python.exe download-model.py %repo%
