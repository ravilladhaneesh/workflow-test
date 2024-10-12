import os

#local
'''
repo_path = os.getcwd()
repo_name = 'dummy'
'''


print('----------------------')
print('TEST GITHUB ACTIONS')
print('----------------------')

repo_name = os.environ.get('REPO_NAME')
repo_path = os.environ.get('REPO_PATH')
repo_url = os.environ.get('REPO_URL')
print(repo_name)
print('---------------------')
print(repo_path)
print('---------------------')
print(repo_url)
print('---------------------')
    
excluded_dirs = {'.git', '.github'}
        
for dirpath, dirnames, filenames in os.walk(repo_path):
    dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
            
    print(f"\nDirectory: {dirpath}")
            
    for file in filenames:
        print(f"  File: {file}")
