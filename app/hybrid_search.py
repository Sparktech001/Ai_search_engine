import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class SearchEngine:
    def __init__(self, function_names):
        self.function_names = function_names
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = self.encoder.encode(function_names, normalize_embeddings=True)
        vectors = np.array(vectors).astype("float32")

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)

    def semantic_search(self, query, threshold=0.5):
        query_vec = self.encoder.encode([query], normalize_embeddings=True).astype("float32")
        scores, indices = self.index.search(query_vec, len(self.function_names))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self.function_names) and score >= threshold:
                results.append({
                    "name": self.function_names[idx],
                    "similarity": float(score)
                })
        return results
