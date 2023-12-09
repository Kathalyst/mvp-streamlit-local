import inspect
import llama2_process
import regex
import replicate
import vault
import os
import github_process
import json
import testing_vdd3

# token = vault.get_Secret("replicate_key")
# os.environ["REPLICATE_API_TOKEN"] = token

prompt_system = """
Identify all functions in the code given in the prompt. Categorize these functions into 2 categories, internal functions or functions defined in the given code, and external functions or functions that are being called from other code files and libraries.
Output all of this information in the format of a JSON defined below:
{
    "filename": filename
    "internal_functions": ["func1", "func2", "func3"],
    "external_functions": ["func4", "func5", "func6"],
    "source_of_external_functions": ["source1","source2","source3"]
}
"""

master_desc = """
from dataclasses import dataclass
import erdantic as erd

class Function:\n\tdef __init__(self, name):\n\t\tself.function_name = name

"""

def create_tables(filename,internal_functions):
    class_desc = """
class Function:
    def __init__(self, name):
        self.function_name = name

class {filename}:
    {internal_functions[0]}: Function """
    for i in range(1,len(internal_functions)):
        class_desc = class_desc + "\n\t{internal_functions[i]}: Function\n\t"
    return class_desc


def extract_json_blobs(content):
    jsons = []
    i = 0
    while i < len(content):
        if content[i] == '{':
            for j in range(len(content) - 1, i, -1):
                if content[j] == '}':
                    try:
                        # yield json.loads(content[i:j+1])
                        print("JSON loads ",json.loads(content[i:j+1]))
                        jsons.append(json.loads(content[i:j+1]))
                        i = j
                        break
                    except json.JSONDecodeError as e:
                        pass
        i += 1
    print("JSONs is \n",jsons)
    return jsons

def identify_functions(file_names,file_contents):
    # system_prompt = "Identify all defined functions in the input coding file. Return a python list with all the function names. Output should be in standard format 'filename: [function 1, function 2, etc.]'"
    system_prompt = prompt_system
    functions = []
    results = []
    for i in range(len(file_names)):
        prompt = file_names[i] + ": \n" + file_contents[i]
        output = llama2_process.custom_prompt(system_prompt,prompt)
        print(type(output))
        print("\nOutput from Llama2:\n",output)
        # matches = regex.extract_matches(output)
        matches = extract_json_blobs(output)
        print("\nPrinting Matches from JSON: ",matches)
        results.append(matches)
        #remove duplicates dictionaries from matches
        # for match in matches:
        #     functions.extend(match['functions'])
        # functions = list(dict.fromkeys(functions))
        # print("Printing functions: ",functions)
    return functions,results

def identify_functions_outside(file_names,file_contents):
    system_prompt = "Identify & List all functions in the input code that is imported or defined in another file or is being called from an external source. Return a python list with all the function names. Output should contain the source of the function in () brackets after the function name."
    functions = []
    results = []
    for i in range(len(file_names)):
        prompt = file_names[i] + ": \n" + file_contents[i]
        output = llama2_process.custom_prompt(system_prompt,prompt)
        print("\n\n\n")
        input = output + output
        matches = regex.extract_matches(input)
        print(matches)
        results.append(matches)
        #remove duplicates dictionaries from matches
        # for match in matches:
        #     functions.extend(match['functions'])
        # functions = list(dict.fromkeys(functions))
        # print(functions)
    return functions,results

# def get_functions(file_path):
#     with open(file_path, 'r') as file:
#         print("Inside open")
#         code = compile(file.read(), file_path, 'exec')
#         print("Code: ",code)
#         print(code.co_varnames)
#         functions = [name for name, obj in inspect.getmembers(code) if inspect.isfunction(obj)]
#         print("Functions: ",functions)
#         return functions
#     # Example usage
#     pass

if __name__ == "__main__":
    
    github_link = "https://github.com/anushkasingh98/test-repo1.git"
    file_contents,file_names,dir = github_process.control(github_link)

    print("File Names\n",file_names)
    print("Count of Num of Files: ",len(file_contents))
    
    functions, matches = identify_functions(file_names,file_contents)

    # functions1, matches1 = identify_functions_outside(file_names,file_contents)

    print("First Round of Matches:\n",matches)
    # print("\nSecond Round of Matches:\n",matches1)

    # print(create_tables("abcd.py",["func1","func2","func3"]))
    print("\nPrinting One By One\n")
    filename = ""
    for match in matches:
        print(match)
        print(type(match))
        for entry in match:
            filename= entry['filename']
            internal_functions = entry['internal_functions']
            external_functions = entry['external_functions']
            source_of_external_functions = entry['source_of_external_functions']
            print("Filename",filename)
            print("Internal Functions",internal_functions)
            print("External Functions",external_functions)
            print("Source of External Functions",source_of_external_functions)
            print("\n\n\n")
        
            master_desc = master_desc + testing_vdd3.create_tables(filename,internal_functions,external_functions,source_of_external_functions)
            print(master_desc)
    
    print("\nFilename:",filename)
    master_desc = master_desc + f"\nerd.draw({filename.split('.')[0]}, out='trial_diagram.png')"
    print(master_desc)
    exec(master_desc)
