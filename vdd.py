import inspect
import os
import subprocess
import re
import javalang
import llama2_process
import github_process

def get_functions(file_path):
    with open(file_path, 'r') as file:
        print("Inside open")
        code = compile(file.read(), file_path, 'exec')
        print("Code: ",code)
        print(code.co_varnames)
        functions = [name for name, obj in inspect.getmembers(code) if inspect.isfunction(obj)]
        print("Functions: ",functions)
        return functions
    # Example usage


if __name__ == "__main__":
    file_path = '/Users/anushkasingh/Library/Group Containers/UBF8T346G9.OneDriveSyncClientSuite/Kathalyst.noindex/Kathalyst/Code/mvp-streamlit-local/hello.py'
    functions = get_functions(file_path)
    print(functions)
