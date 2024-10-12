import os

print('----------------------')
print('TEST GITHUB ACTIONS')
print('----------------------')

repo_name = os.environ.get('REPO_NAME')
repo_path = os.environ.get('REPO_PATH')
print(repo_name)
print('---------------------')
print(repo_path)
print('---------------------')



