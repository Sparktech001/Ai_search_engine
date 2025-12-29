import os 
import json
import ast 
import builtins

py_paths = []
def read_repo(folder_path):
    for root, dirs, filesw in os.walk(folder_path):
        for file in filesw:
            if file.endswith(".py"):
                py_paths.append(os.path.join(root, file))

read_repo(r"C:\Users\Joseph Dania\Desktop\python_repo")

built_ins = {name for name in dir(builtins)}
class Function_finder(ast.NodeVisitor):
    def __init__(self):
        self.function_stack = []
        self.calls = {}

    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.calls[node.name] = []
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_Call(self, node):
        if self.function_stack:
            #dfs last in first out
            caller = self.function_stack[-1]
            if isinstance(node.func, ast.Name):
                callee = node.func.id
                if callee not in built_ins:
                    self.calls[caller].append(callee)
        self.generic_visit(node)

global_graph = {}

for path in py_paths:
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        code = file.read()
        try:
            tree = ast.parse(code)
        except (SyntaxError, UnicodeDecodeError):
            continue

        finder = Function_finder()
        finder.visit(tree)
    for func, calls in finder.calls.items():
        if func not in global_graph:
            global_graph[func] = []
        global_graph[func].extend(calls)

with open(r"C:\Users\Joseph Dania\Desktop\Ai_search_engine\doc\function_graph.json", "w") as files:
    write = json.dump(global_graph, files, indent=4)

first_key = list(global_graph.values())[0]
print(f"First key: {first_key}")

