import llama2_process
import github_process
import json
import graph_order

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

defined_classes = []
all_classes = []

def create_tables(filename,internal_functions,external_functions,source):
    funcs = []
    correction_num = 1
    mod_filename = filename.split('.')[0]
    if('/' in mod_filename):
        mod_filename = mod_filename.split('/')[0]
    mod_filename.replace(" ","_")
    mod_filename.strip()
    mod_filename = mod_filename.replace(":","")
    
    class_desc = f"""
@dataclass
class {filename.split('.')[0]}: """
    
    defined_classes.append(mod_filename)
    
    if len(external_functions) != len(source):
        if len(external_functions) > len(source):
            print("Source is smaller")
            for i in range(len(source),len(external_functions)):
                source.append("Source_Unknown")
        else:
            print("External Functions is smaller")
            for i in range(len(external_functions),len(source)):
                external_functions.append("N/A")

    for i in range(len(internal_functions)):
        mod_func = internal_functions[i]
        if('.' in mod_func):
            mod_func = mod_func.split('.')[-1]
        if('/' in mod_func):
            mod_func = mod_func.split('/')[0]
        mod_func.replace(" ","")
        mod_func.strip()

        if mod_func in funcs:
            mod_func += str(correction_num)
            correction_num += 1

        funcs.append(mod_func)

        class_desc = class_desc + f"\n\t{mod_func}: Function\n\t"

    for i in range(len(external_functions)):
        mod_func = external_functions[i]
        if('.' in mod_func):
            mod_func = mod_func.split('.')[-1]
        if('/' in mod_func):
            mod_func = mod_func.split('/')[0]
        mod_func.replace(" ","")
        if mod_func in funcs:
            mod_func += str(correction_num)
            correction_num += 1
        funcs.append(mod_func)

        mod_source = source[i]
        mod_source = mod_source.replace(" ","")
        mod_source = mod_source.split('.')[0]
        mod_source = mod_source.split('/')[0]

        class_desc = class_desc + f"\n\t{mod_func}: {mod_source}\n\t"
        all_classes.append(mod_source)
    print(class_desc)
    return class_desc

def post_processing(defined_classes,all_classes,master_desc):
    print("Defined Classes: ",defined_classes)
    print("All Classes: ",all_classes)

    defined_classes = list(set(defined_classes))
    all_classes = list(set(all_classes))

    for i in range(len(all_classes)):
        if all_classes[i] not in defined_classes:
            print("Class ",all_classes[i]," is not defined in the code. Creating a class for it.")
            master_desc = master_desc + f"\nclass {all_classes[i]}:\n\tdef __init__(self, name):\n\t\tself.function_name = name"
    print("Master Desc: ",master_desc)
    return master_desc

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
    return functions,results

def process_control(file_contents,file_names,image_filename):
    master_desc = """
from dataclasses import dataclass
import erdantic as erd

class Function:\n\tdef __init__(self, name):\n\t\tself.function_name = name

"""
    
    print("Inside VDD Control")
    functions, matches1 = identify_functions(file_names,file_contents)

    # functions1, matches1 = identify_functions_outside(file_names,file_contents)
    matches = graph_order.new_order_for_processing(matches1)
    print("First Round of Matches:\n",matches)
    # print("\nSecond Round of Matches:\n",matches1)

    # print(create_tables("abcd.py",["func1","func2","func3"]))
    print("\nPrinting One By One\n")
    filename = ""

    class_desc = []

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
        
            class_desc.append(create_tables(filename,internal_functions,external_functions,source_of_external_functions))
    
    print("\nFilename:",filename)
    master_desc = post_processing(defined_classes,all_classes,master_desc)

    for desc in class_desc:
        master_desc = master_desc + desc

    master_desc = master_desc + f"\nerd.draw({filename.split('.')[0]}, out='{image_filename}.png')"
    print("Master Desc:\n",master_desc)
    exec(master_desc)
    ret = image_filename + ".png"
    return ret

if __name__ == "__main__":
    
    github_link = "https://github.com/anushkasingh98/test-repo1.git"
    file_contents,file_names,dir = github_process.control(github_link)

    print("File Names\n",file_names)
    print("Count of Num of Files: ",len(file_contents))
    
    process_control(file_contents,file_names,"diagram_trial")
