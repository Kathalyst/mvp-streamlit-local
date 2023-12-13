# run a terminal command "dbml-renderer -i example.dbml -o output.svg" in python
import subprocess

# run the command "npm install -g @softwaretechnik/dbml-renderer" in python
# subprocess.run(["npm", "install", "-g", "@softwaretechnik/dbml-renderer"])

subprocess.run(["dbml-renderer", "-i", "example.dbml", "-o", "output.svg"])

