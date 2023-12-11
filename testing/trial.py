from dataclasses import dataclass
import erdantic as erd

class Function:
        def __init__(self, name):
                self.function_name = name


class Source_Unknown:
        def __init__(self, name):
                self.function_name = name
class zipfile:
        def __init__(self, name):
                self.function_name = name
class os:
        def __init__(self, name):
                self.function_name = name
class source1:
        def __init__(self, name):
                self.function_name = name
class module:
        def __init__(self, name):
                self.function_name = name
class shutil:
        def __init__(self, name):
                self.function_name = name
# class global:
#         def __init__(self, name):
#                 self.function_name = name
class source2:
        def __init__(self, name):
                self.function_name = name
class source3:
        def __init__(self, name):
                self.function_name = name
@dataclass
class master: 
        getName: Function

        sayHello: Function

        require: module

        # log: global

@dataclass
class main: 
        func1: Function

        func2: Function

        func3: Function

        func4: source1

        func5: source2

        func6: source3

@dataclass
class app2: 
        extract_zip: Function

        collect_contents: Function

        create_output_file: Function

        process_zip_file: Function

        ZipFile: zipfile

        listdir: os

        isfile: shutil

        open: Source_Unknown

        read: Source_Unknown

        write: Source_Unknown

        makedirs: Source_Unknown

        rmtree: Source_Unknown

erd.draw(app2, out='diagram.png')