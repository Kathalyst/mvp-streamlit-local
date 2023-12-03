import inspect
import llama2_process
import regex

def identify_functions(file_names,file_contents):
    system_prompt = "Identify all defined functions in the input coding file. Return a python list with all the function names. Output should be in standard format 'filename: [function 1, function 2, etc.]'"
    functions = []
    for i in range(len(file_names)):
        prompt = file_names[i] + ": \n" + file_contents[i]
        output = llama2_process.custom_prompt(system_prompt,prompt)
        print("\n\n\n")
        print(output)
        matches = regex.extract_matches(output)
    pass

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
    file_path = '/Users/anushkasingh/Library/Group Containers/UBF8T346G9.OneDriveSyncClientSuite/Kathalyst.noindex/Kathalyst/Code/mvp-streamlit-local/vault.py'
    with open(file_path, 'r',  encoding='latin-1') as f:
        contents = f.read()
        file_name = "hello.py"
        file_names = [file_name]
        file_contents = [contents]
    identify_functions(file_names,file_contents)
