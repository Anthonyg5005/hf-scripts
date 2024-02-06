from huggingface_hub import login, get_token, create_branch

login(get_token())

create_branch('Anthonyg5005/rishiraj-meow-10.7B-exl2', repo_type='model', branch='8bit')