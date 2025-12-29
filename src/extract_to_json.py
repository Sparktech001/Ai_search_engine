import ast
import json
import builtins
import os


py_path = []
def read_repo(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                py_path.append(os.path.join(root, file))

read_repo(r"C:\Users\Joseph Dania\Desktop\python_repo")

built_ins = {name for name in dir(builtins)}

class Function_Finder(ast.NodeVisitor):
    def __init__(self, filename, source_code):
        self.filename = filename
        self.source_code = source_code
        self.data = []

    def visit_FunctionDef(self, node):
        doc_string = ast.get_docstring(node)

        source_code = ast.get_source_segment(self.source_code, node)

        function_info = {
            "name": node.name,
            "docstring": doc_string,
            "code": source_code,
            "file": self.filename,
            "line_start": node.lineno,
            "line_stop": node.end_lineno,
        }

        self.data.append(function_info)

        self.generic_visit(node)

all_functions = []

for file_path in py_path:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()

            tree = ast.parse(source)

            finder = Function_Finder(file_path, source)
            finder.visit(tree)

            all_functions.extend(finder.data)
    
    except Exception as e:
        print(f"Could not prase {file_path}: {e}")

with open(r"C:\Users\Joseph Dania\Desktop\Ai_search_engine\doc\func_docstring.json", "w") as file:
    write = json.dump(all_functions, file, indent=2)