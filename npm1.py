# run a terminal command "dbml-renderer -i example.dbml -o output.svg" in python
import subprocess

# run the command "npm install -g @softwaretechnik/dbml-renderer" in python
# subprocess.run(["npm", "install", "-g", "@softwaretechnik/dbml-renderer"])

# subprocess.run(["dbml-renderer", "-i", "example.dbml", "-o", "output.svg"])

def install_npm():
    # run command curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
    subprocess.run(["curl", "-o-", "https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash"])
    # print(subprocess.getoutput('curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -'))

    # import os
    # home = os.environ['HOME']
    # print("\n\n")
    # print(home)
    # print("\n\n")
    # os.environ["NVM_DIR"] = home+"/.nvm"
    # subprocess.run(['export','NVM_DIR="$HOME/.nvm"'])
    # run command nvm install node
    # subprocess.run(["nvm", "install", "node"])
    # run command sudo apt-get update 
    subprocess.run(['sudo','apt-get','update'])
    subprocess.run(['sudo','apt-get','install','nodejs'])
    subprocess.run(['sudo','apt-get','install','npm'])
    # sudo apt-get install nodejs 
    # sudo apt-get install npm 

    subprocess.run(["npm", "install", "-g", "@softwaretechnik/dbml-renderer"])

if __name__ == "__main__":
    install_npm()