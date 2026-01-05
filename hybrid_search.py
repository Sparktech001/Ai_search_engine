import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os



class Node:
    def __init__(self):
        self.children = {}
        self.is_complete = False


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_complete = True

    def autocomplete(self, prefix):
        results = []
        node = self.root

        for char in prefix:
            if char not in node.children:
                return results
            node = node.children[char]

        def dfs(current, path):
            if current.is_complete:
                results.append("".join(path))
            for c, child in current.children.items():
                dfs(child, path + [c])

        dfs(node, list(prefix))
        return results



def load_function_names(csv_path="raw_code.csv"):
    if not os.path.exists(csv_path):
        return [
            "get_user",
            "get_id",
            "delete_account",
            "remove_user",
            "fetch_data",
            "calculate_tax",
        ]

    data = pd.read_csv(csv_path)
    calls = data["Function Calls"].dropna().astype(str)

    unique = set()
    for row in calls:
        for fn in row.split(","):
            fn = fn.strip()
            if fn:
                unique.add(fn)

    return list(unique)


class SearchEngine:
    def __init__(self, function_names):
        self.function_names = function_names

        self.trie = Trie()
        for name in function_names:
            self.trie.insert(name)

        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = self.encoder.encode(function_names)

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors))

        print(f"Indexed {len(function_names)} functions")

    def prefix_search(self, query):
        return self.trie.autocomplete(query)

    def semantic_search(self, query, top_k=5):
        query_vec = self.encoder.encode([query])
        _, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.function_names):
                results.append(self.function_names[idx])
        return results

    def search(self, query):
        prefix_results = self.prefix_search(query)
        semantic_results = self.semantic_search(query)

        seen = set()
        combined = []

        for item in prefix_results + semantic_results:
            if item not in seen:
                combined.append(item)
                seen.add(item)

        return combined



if __name__ == "__main__":
    functions = load_function_names()
    engine = SearchEngine(functions)

    while True:
        query = input("\nSearch (q to quit): ").strip()
        if query.lower() == "q":
            break

        results = engine.search(query)

        if not results:
            print("No matches found")
            continue

        for i, name in enumerate(results, 1):
            label = "PREFIX" if name.startswith(query) else "SIMILAR"
            print(f"{i}. {name} [{label}]")
