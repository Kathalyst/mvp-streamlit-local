from dataclasses import dataclass
import erdantic as erd

class Function:
        def __init__(self, name):
                self.function_name = name

class zipfile:
        def __init__(self, name):
                self.function_name = name
class shutil:
        def __init__(self, name):
                self.function_name = name
class Source_Unknown:
        def __init__(self, name):
                self.function_name = name
class os:
        def __init__(self, name):
                self.function_name = name
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