


def create_tables(filename,internal_functions,external_functions,source):
    class_desc = f"""
@dataclass
class {filename.split('.')[0]}: """
    
    if len(external_functions) != len(source):
        print("The length of Source & length of External Functions DO NOT MATCH.\n")
        print("Length of External Functions = ",len(external_functions))
        print("Length of Source = ",len(source))
        print("\n")
        print(external_functions)
        print("\n")
        print(source)
        print("\n")
        if len(external_functions) > len(source):
            print("Source is smaller")
            for i in range(len(source),len(external_functions)):
                source.append("None")
        else:
            print("External Functions is smaller")
            for i in range(len(external_functions),len(source)):
                external_functions.append("N/A")

    for i in range(len(internal_functions)):
        class_desc = class_desc + f"\n\t{internal_functions[i]}: Function\n\t"

    for i in range(len(external_functions)):
        class_desc = class_desc + f"\n\t{external_functions[i]}: {source[i].split('.')[0]}\n\t"
    
    # class_desc = class_desc + f"\nerd.draw({filename.split('.')[0]}, out='diagram_exec.png')"
    print(class_desc)
    return class_desc

if __name__ == "__main__":

    exec(create_tables("abcd.py",["func1","func2","func3"],[],[]))