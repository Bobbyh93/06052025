import math
import os
import pickle
from typing import List


class SimpleIndex:
    def __init__(self, dim: int, index_path: str, persist: bool = True):
        self.dim = dim
        self.index_path = index_path
        self.persist = persist
        self.embeddings: List[List[float]] = []
        self.docs: List = []
        if persist and os.path.exists(index_path):
            self._load()

    def add(self, embeddings: List[List[float]], docs: List):
        self.embeddings.extend(embeddings)
        self.docs.extend(docs)
        if self.persist:
            self._save()

    def search(self, query_embedding: List[float], top_k: int = 5):
        distances = []
        for i, emb in enumerate(self.embeddings):
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(emb, query_embedding)))
            distances.append((dist, i))
        distances.sort(key=lambda x: x[0])
        return [self.docs[i] for (_, i) in distances[:top_k]]

    def _save(self):
        with open(self.index_path, "wb") as f:
            pickle.dump({"embeddings": self.embeddings, "docs": self.docs}, f)

    def _load(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)
                self.embeddings = data.get("embeddings", [])
                self.docs = data.get("docs", [])
