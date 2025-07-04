class SimpleEmbedder:
    """Very small embedding model using character counts."""

    def _embed(self, text: str):
        vec = [0] * 26
        for ch in text.lower():
            if 'a' <= ch <= 'z':
                vec[ord(ch) - 97] += 1
        return vec

    def embed_documents(self, texts):
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        return self._embed(text)
