class RAGPipeline:
    """Tiny RAG pipeline using only standard library components."""

    def __init__(self, loader, embedder, index, retriever, llm):
        self.loader = loader
        self.embedder = embedder
        self.index = index
        self.retriever = retriever
        self.llm = llm

    def build(self):
        docs = self.loader.load()
        texts = [doc.page_content for doc in docs]
        embeddings = self.embedder.embed_documents(texts)
        self.index.add(embeddings, docs)

    def query(self, question: str):
        docs = self.retriever.retrieve(question)
        context = "\n".join(doc.page_content for doc in docs)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        return self.llm.generate(prompt)
