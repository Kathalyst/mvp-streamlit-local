# run a terminal command "dbml-renderer -i example.dbml -o output.svg" in python
import subprocess

# run the command "npm install -g @softwaretechnik/dbml-renderer" in python
# subprocess.run(["npm", "install", "-g", "@softwaretechnik/dbml-renderer"])

# subprocess.run(["dbml-renderer", "-i", "example.dbml", "-o", "output.svg"])

def install_npm():
    # run command curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
    subprocess.run(["curl", "-o-", "https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh", "|", "bash"])
    # run command nvm install node
    subprocess.run(["nvm", "install", "node"])
    subprocess.run(["npm", "install", "-g", "@softwaretechnik/dbml-renderer"])