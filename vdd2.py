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

def correct_name(name):
    mod_name = name.strip()
    mod_name = mod_name.replace(" ","_")
    # mod_name = mod_name.replace(".","_")
    mod_name = mod_name.replace(":","")
    return mod_name

def assimilating_functions(matches):
    new_matches = {}
    for match in matches:
        for entry in match:
            filename = entry['filename']
            internal_functions = entry['internal_functions']
            new_matches[filename] = internal_functions
    return new_matches

def create_DBML(matches):
    statements_connections = ""
    table_desc = ""
    master_desc = ""

    fil_internal_funcs = assimilating_functions(matches)
    print("Printing Fil Internal Funcs: ",fil_internal_funcs)

    correctional_num = 0

    for match in matches:
        if len(match) == 0:
            continue
        for entry in match:
            processed_functions = []
            table_desc = ""
            filename = entry['filename']
            external_functions = entry['external_functions']
            internal_functions = entry['internal_functions']

            table_desc = "\nTable " + str(filename) + " {\n"

            for f in internal_functions:
                if f in processed_functions:
                    table_desc = table_desc + f"{f}{correctional_num} Function\n"
                    correctional_num += 1
                else:
                    table_desc = table_desc + f"{f} Function\n"
                processed_functions.append(f)

            for source in entry['source_of_external_functions']:
                # check if source is a key in the dictionary fil_internal_funcs
                if source in fil_internal_funcs.keys():
                    # if yes, then find the value in external_functions that is in fil_internal_funcs[source]
                    for func in external_functions:
                        if func not in fil_internal_funcs[source]:
                            external_functions.remove(func)
                        else:
                            # func is in source. Create statement from [source,func] to [filename,func]
                            if func in processed_functions:
                                table_desc = table_desc + f"{func}{correctional_num} External_Function\n"
                                statements_connections = statements_connections + f"\nRef: {source}.{func} - {filename}.{func}{correctional_num}"
                                correctional_num += 1
                            else:
                                table_desc = table_desc + f"{func} External_Function\n"
                                statements_connections = statements_connections + f"\nRef: {source}.{func} - {filename}.{func}"
                            processed_functions.append(func)
                else:
                    pass
            
            table_desc = table_desc + "}"
            print(table_desc)
            master_desc = master_desc + table_desc
    
    master_desc = master_desc + "\n" + statements_connections
    print("Master Desc: ",master_desc)
    return master_desc

def check_names(matches):
    for match in matches:
        for entry in match:
            #correcting the filename/tablename
            filename = entry['filename']
            mod_filename = correct_name(filename)
            mod_filename = mod_filename.split('.')[0]
            if('/' in mod_filename):
                mod_filename = mod_filename.split('/')[0]
            entry['filename'] = mod_filename

            #correcting the internal function names
            for i in range(len(entry['internal_functions'])):
                func = entry['internal_functions'][i]
                mod_func = correct_name(func)
                if('.' in mod_func):
                    mod_func = mod_func.split('.')[-1]
                if('/' in mod_func):
                    mod_func = mod_func.split('/')[0]
                entry['internal_functions'][i] = mod_func

            for i in range(len(entry['external_functions'])):
                func = entry['external_functions'][i]
                mod_func = correct_name(func)
                if('.' in mod_func):
                    mod_func = mod_func.split('.')[-1]
                if('/' in mod_func):
                    mod_func = mod_func.split('/')[0]
                entry['external_functions'][i] = mod_func
            
            for i in range(len(entry['source_of_external_functions'])):
                src = entry['source_of_external_functions'][i]
                mod_src = correct_name(src)
                mod_src = mod_src.split('.')[0]
                if('/' in mod_src):
                    mod_src = mod_src.split('/')[0]
                entry['source_of_external_functions'][i] = mod_src
    return matches

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

def vdd_file_creation(file_contents,file_names,dbml_filename):
    master_desc = ""
    
    print("Inside VDD Creation Code")
    functions, matches1 = identify_functions(file_names,file_contents)
    
    matches = graph_order.new_order_for_processing(matches1)

    matches = check_names(matches)
    print("First Round of Matches:\n",matches)
    # print("\nSecond Round of Matches:\n",matches1)

    # print(create_tables("abcd.py",["func1","func2","func3"]))
    print("\nPrinting One By One\n")
    master_desc = create_DBML(matches)
    
    # write master_desc string to file vdd.dbml and Create vdd.dbml if file does not exist
    with open(dbml_filename + ".dbml","w") as f:
        f.write(master_desc)

    ret = dbml_filename + ".dbml"
    return ret

if __name__ == "__main__":
    
    github_link = "https://github.com/anushkasingh98/testing-repo2"
    file_contents,file_names,dir = github_process.control(github_link)

    print("File Names\n",file_names)
    print("Count of Num of Files: ",len(file_contents))
    
    ret = vdd_file_creation(file_contents,file_names,"diagram_trial")

    import subprocess

    subprocess.run(["dbml-renderer", "-i", "diagram_trial.dbml", "-o", "diagram_trial.svg"])
