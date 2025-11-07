import os
import ast
import csv 

def analyze_repo(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results = []

    def get_func_name(node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return get_func_name(node.value) + '.' + node.attr
        return ''

    for node in ast.walk(tree):
        # Classes
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_doc = (ast.get_docstring(node) or "").replace("\n", " ").strip()
            results.append([file_path, class_name, "", class_doc, ""])

        # Functions
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_doc = (ast.get_docstring(node) or "").replace("\n", " ").strip()

            calls = []
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    calls.append(get_func_name(child.func))

            if func_name or calls:
                results.append([file_path, "", func_name, func_doc, ", ".join(calls)])

    return results




def walk_repo(repo_path):
    all_results = []
    for root, dir, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                all_results.extend(analyze_repo(full_path))

    return all_results

def save_csv(data, csv_file="raw_code.csv"):
    headers = ["File", "Class", "Function", "Docstring", "Function Calls"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)
        for row in data:
            clean_row = [col if col else "" for col in row]
            writer.writerow(clean_row)



def main():
    repo_path = "C:/Users/Joseph Dania/Desktop/python_repo"
    extracted_data = walk_repo(repo_path)
    save_csv(extracted_data)
    print(f"COMPLETE!")

if __name__ == "__main__":
    main()
