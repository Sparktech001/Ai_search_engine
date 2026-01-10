import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def load_function_names(csv_path=r"C:\Users\Joseph Dania\Desktop\Ai_search_engine\raw_code.csv"):
    if not os.path.exists(csv_path):
        return [
            "Function Calls",
            "Docstring",
            "Function",
            "Class"
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

        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = self.encoder.encode(function_names, normalize_embeddings=True)
        vectors = np.array(vectors).astype("float32")

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)

        print(f"Indexed {len(function_names)} functions")

    def semantic_search(self, query, threshold=0.5):
        query_vec = self.encoder.encode([query], normalize_embeddings=True).astype("float32")
        # search for all entries
        scores, indices = self.index.search(query_vec, len(self.function_names))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self.function_names) and score >= threshold:
                results.append({
                    "name": self.function_names[idx],
                    "similarity": float(score)
                })
        return results

if __name__ == "__main__":
    functions = load_function_names()
    engine = SearchEngine(functions)

    while True:
        query = input("\nSearch (q to quit): ").strip()
        if query.lower() == "q":
            break

        results = engine.semantic_search(query)
        if not results:
            print("No matches found")
            continue

        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']} similarity: {r['similarity']:.3f}")
