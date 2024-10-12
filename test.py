import os

print('----------------------')
print('TEST GITHUB ACTIONS')
print('----------------------')

repo_name = os.environ.get('REPO_NAME')
repo_url = os.getcwd()
print(repo_name)
print('---------------------')
print(repo_url)
print('---------------------')



