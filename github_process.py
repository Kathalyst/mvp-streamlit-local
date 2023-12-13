import os
import subprocess
import file_data

ignore_file_types = [".png",".img",".csv",".ipynb",".MD",".md",".JPG",".jpg",".pyc",".sqlite3",".sample",".pack",".idx",".wav",".svg",".ttf"]
ignore_file_names = ["HEAD","main","master","exclude","config","index","description","packed-refs"]

def clone_repo(github_link,directory):
    # Extract the repository name from the GitHub link
    repo_name = github_link.split("/")[-1].replace(".git", "")
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    path = os.path.join(directory, repo_name)

    # if path exists, empty the directory psth
    if os.path.exists(path):
        # unlink all files in path 
        # print("Emptying directory ... ",path)
        # for filename in os.listdir(path):
        #     file_path = os.path.join(path, filename)
        #     try:
        #         if os.path.isfile(file_path) or os.path.islink(file_path):
        #             os.unlink(file_path)
        #     except Exception as e:
        #         print('Failed to delete %s. Reason: %s' % (file_path, e))
        # #delete folder in path and all files in it
        print("Deleting directory ... ",path)
        from pathlib import Path
        from shutil import rmtree

        for p in Path(path).glob("**/*"):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                rmtree(p)

    # Clone the repository to the specified directory
    subprocess.run(["git", "clone", github_link, path])
    dir = os.path.join(directory, repo_name)
    print("\n Directory after clone_repo: ",dir)
    return dir

def read_files_in_directory(directory, file_contents, file_names):
    print("Directory : ",directory)
    skipped_files=0
    total_files = 0
    i = 0
    for root, dirs, files in os.walk(directory):
        for file in [f for f in files if not f[0] == '.']:
            total_files += 1
            file_path = os.path.join(root, file)
            print("Trying to Read File: ", file)
            #ignore files with ext in ignore_file_types
            if any(ext in file for ext in ignore_file_types):
                skipped_files += 1
                continue
            #if filename of file is in ignore_file_names, skip file
            if any(name in file for name in ignore_file_names):
                skipped_files += 1
                continue
            with open(file_path, 'r',  encoding='latin-1') as f:
                contents = f.read()
                print("Reading File: ", file)
                # print(contents)
                file_contents.append(contents)
                file_names.append(file)
    print("\nTotal Files: ",total_files)
    print("Skipped Files: ",skipped_files)
    return file_contents, file_names

def remove_empty_files(file_names,file_contents):
    length = len(file_names)
    list_pop = []
    #remove empty strings from file_contents
    for i in range(length):
        if file_contents[i] == "":
            list_pop.append(i)
    list_pop.sort(reverse=True)
    for i in list_pop:
        file_contents.pop(i)
        file_names.pop(i)
    return file_contents,file_names

def control(github_repo):
    current_directory = os.getcwd()
    directory = os.path.join(current_directory, r'Git-Processing-Folder')
    if not os.path.exists(directory):
        os.makedirs(directory)

    # clone repo to directory
    dir = clone_repo(github_repo,directory)

    # read files in directory and create prompt
    file_contents = []
    file_names = []
    file_contents, file_names = read_files_in_directory(dir,file_contents,file_names)
    file_contents, file_names = remove_empty_files(file_names,file_contents)

    return file_contents,file_names,dir

if __name__ == "__main__":
    github_link = "https://github.com/Kathalyst/TaskManager"
    current_directory = os.getcwd()
    directory = os.path.join(current_directory, r'Git-Processing-Folder')
    if not os.path.exists(directory):
        os.makedirs(directory)
    dir = clone_repo(github_link,directory)