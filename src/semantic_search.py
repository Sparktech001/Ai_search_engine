# semantic_search.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ---- lazy-loaded globals ----
_model = None
_index = None
_metadata = None

def _load():
    global _model, _index, _metadata
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _index = faiss.read_index("embeddings.index")

        with open("metadata.json", "r", encoding="utf-8") as f:
            _metadata = json.load(f)

def search_ai(query: str, top_k: int = 5):
    _load()  # runs ONLY once

    q = _model.encode([query], normalize_embeddings=True)
    q = np.array(q).astype("float32")

    scores, ids = _index.search(q, top_k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        item = _metadata[idx]
        results.append({
            "name": item["name"],
            "file": item["file"],
            "score": float(score),
        })

    return results
