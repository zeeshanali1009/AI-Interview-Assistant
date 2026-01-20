import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store(texts):
    chunks = []
    for text in texts:
        parts = [text[i:i+500] for i in range(0, len(text), 500)]
        chunks.extend(parts)

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings, chunks

def query_vector_store(query, index, embeddings, texts, k=3):
    query_vector = model.encode([query]).astype("float32")
    _, indices = index.search(query_vector, k)
    return " ".join([texts[i] for i in indices[0]])
