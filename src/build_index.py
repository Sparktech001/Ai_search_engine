# build_index.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(r"C:\Users\Joseph Dania\Desktop\Ai_search_engine\doc\func_docstring.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [
    f"{x['name']}\n{x['docstring']}\n{x['code']}"
    for x in data
]

embeddings = model.encode(
    texts,
    batch_size=32,
    normalize_embeddings=True,
    show_progress_bar=True,
)

embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "embeddings.index")

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

print(f"Indexed {len(data)} functions")
