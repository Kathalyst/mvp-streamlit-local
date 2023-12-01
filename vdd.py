import inspect

def get_functions(file_path):
    with open(file_path, 'r') as file:
        code = compile(file.read(), file_path, 'exec')
        functions = [name for name, obj in inspect.getmembers(code) if inspect.isfunction(obj)]
        return functions

# Example usage
file_path = '/Users/anushkasingh/Library/Group Containers/UBF8T346G9.OneDriveSyncClientSuite/Kathalyst.noindex/Kathalyst/Code/mvp-streamlit-local/hello.py'
functions = get_functions(file_path)
print(functions)
