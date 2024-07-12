# Script Packager v1.1
# This script will package all python files in the current directory into one file
# Author: JMcrafter26

import os
import shutil # pip install shutil
import python_minifier # pip install python-minifier
import git # pip install GitPython

minifyRenameVars = False
removeComments = True

# Put the files that you want to include in the program here
# first file in list will be the main file
programAllowed = [
    'main_server.py',
    'packets.py',
    'protocol.py',
    'regex_patterns.py',
    'socket_handler.py',
]

# get the first file in the list of allowed files
if len(programAllowed) > 0:
    firstFile = programAllowed[0]
else:
    firstFile = 'main'

# remove '.py' from the first file
firstFile = firstFile.replace('.py', '')

print(firstFile)
# exit()

# clear terminal
os.system('cls' if os.name == 'nt' else 'clear')
print("Script Packager \n")
print("This script will package all python files in the current directory into one file\n")
print("Author: JMcrafter26\n\n")


release = os.getcwd() + '/release/'
version = ''

# create the release directory
if not os.path.exists(release):
    os.makedirs(release)

programReleaseRaw = release + '/program-raw/' + version.replace('.', '') + '/'
if not os.path.exists(programReleaseRaw):
    os.makedirs(programReleaseRaw)

# clear the program release directory
for file in os.listdir(programReleaseRaw):
    os.remove(os.path.join(programReleaseRaw, file))


# only copy the allowed files in root, no subdirectories
for file in programAllowed:
    if os.path.exists(file):
        shutil.copy2(file, programReleaseRaw)

print('Merging files ...')
oneFileFiles = []
with open(os.path.join(programReleaseRaw, 'tempPackFile.py'), 'w') as file:
    for root, dirs, files in os.walk(programReleaseRaw):
        for file_name in files:
            if file_name != 'tempPackFile.py' and file_name.endswith('.py') and file_name != firstFile + '.py':
                with open(os.path.join(root, file_name), 'r') as f:
                    oneFileFiles.append(file_name.replace('.py', ''))
                    # before writing the file, add a comment with the file name
                    file.write(f'#! {file_name}\n')
                    file.write(f.read())
                    file.write('\n\n\n')

# include main.py at the end of the file
with open(os.path.join(programReleaseRaw, firstFile + '.py'), 'r') as file:
    file = file.read()
    with open(os.path.join(programReleaseRaw, 'tempPackFile.py'), 'a') as f:
        f.write(file)
        oneFileFiles.append('main')

print('Cleaning up the file ...')
# analyze the tempPackFile.py file and remove duplicate imports and imports that import other files in the dir, e.g. import main refers to main.py
with open(os.path.join(programReleaseRaw, 'tempPackFile.py'), 'r') as file:
    lines = file.readlines()

# remove duplicate imports
imports = []
for i, line in enumerate(lines):
    if 'import' in line:
        if line not in imports:
            imports.append(line)
        else:
            lines[i] = ''

# remove imports that import other files in the dir
for i, line in enumerate(lines):
    if 'import' in line:
        for file in oneFileFiles:
            if file.split('.')[0] in line:
                lines[i] = ''
        

# remove the name of module functions that are in oneFileFiles , e.g. functions.function() -> function()
for i, line in enumerate(lines):
    for file in oneFileFiles:
        if lines[i].replace(f'{file}.', ''):
            # get the start and end position of the function name in the line, e.g. functions.function() -> (11, 19)
            start = lines[i].find(f'{file}.')
            end = start + len(f'{file}.')
            # check if at the end of the function is py
            if not lines[i][end:end+2] == 'py' and not lines[i][end:end+3] == 'bat' and not lines[i][end:end+3] == 'exe' and not lines[i][end:end+4] == 'json' and not lines[i][end:end+3] == 'txt' and not lines[i][end:end+3] == 'bak' and not lines[i][end:end+3] == 'zip' and not lines[i][end:end+4] == 'html' and not lines[i][end:end+3] == 'log':
                lines[i] = lines[i].replace(f'{file}.', '')

# get all imports and move them to the top of the file
imports = []
for i, line in enumerate(lines):
    if 'import' in line:
        imports.append(line)
        lines[i] = ''
    
# add the imports to the top of the file
for i, line in enumerate(imports):
    lines.insert(i, line)
lines.insert(len(imports), '\n')



# # remove comments
if removeComments:
    # remove all comments (except that start with #! instead of #)
    for i, line in enumerate(lines):
        if '#' in line and not '#!' in line:
            lines[i] = ''

# remove empty lines if they stretch for more than 2 lines
for i, line in enumerate(lines):
    if lines[i] == '\n' and lines[i+1] == '\n':
        lines[i] = ''

print('Getting the project information ...')
name = ''
description = ''
url = ''
author = ''
license = ''

# get the name from the .git folder, if it exists, if not, use the current directory name
if os.path.exists('.git'):
    repo = git.Repo(os.getcwd())
elif os.path.exists('../.git'):
    repo = git.Repo(os.path.join(os.getcwd(), '..'))

if os.path.exists('.git') or os.path.exists('../.git'):
    name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    author = repo.remotes.origin.url.split('/')[-2]
    description = repo.description
    url = repo.remotes.origin.url

else:
    name = os.path.basename(os.getcwd())

print(f'{name} by {author}')

if name != '':
    name = name.replace('-', ' ').replace('_', ' ').title()
    comment = f'# {name}\n'
if author != '':
    comment += f'# Author: {author}\n'
if description != '' and description != 'Unnamed repository; edit this file \'description\' to name the repository.':
    comment += f'# Description: {description}\n'
if url != '':
    comment += f'# URL: {url}\n'
if license != '':
    comment += f'# License: {license}\n\n\n'



print('Creating minified file ...')

# minify file using pyminify
minified = python_minifier.minify(''.join(lines), rename_globals=minifyRenameVars)
minified = python_minifier.minify(minified, remove_literal_statements=True)
# minified = ''.join(lines)
minified = '\n# This code was minified to save space. If you want to read the code, please read the original files.\n\n\n' + minified

minified = comment + minified

programRelease = release + '/program/' + version.replace('.', '') + '/'
if not os.path.exists(programRelease):
    os.makedirs(programRelease)



# write the minified file to mian.min.py
with open(os.path.join(programRelease, f'{firstFile}.min.py'), 'w') as file:
    file.write(minified)

# write the original file to main.py
with open(os.path.join(programRelease, f'{firstFile}.py'), 'w') as file:
    file.write(comment + '\n\n\n' + ''.join(lines))


os.remove(os.path.join(programReleaseRaw, 'tempPackFile.py'))
print('Done!')
exit()
