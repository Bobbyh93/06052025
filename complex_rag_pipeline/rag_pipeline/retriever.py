class Retriever:
    def __init__(self, index, embedder, top_k: int = 5):
        self.index = index
        self.embedder = embedder
        self.top_k = top_k

    def retrieve(self, query: str):
        query_emb = self.embedder.embed_query(query)
        return self.index.search(query_emb, top_k=self.top_k)
