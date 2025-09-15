from dataclasses import dataclass
import os


@dataclass
class Document:
    page_content: str


class DocumentLoader:
    """Load .txt files from a directory and split them into chunks."""

    def __init__(self, docs_path: str, chunk_size: int = 512, chunk_overlap: int = 50):
        self.docs_path = docs_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _split_text(self, text: str):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(Document(page_content=chunk))
            start = end - self.chunk_overlap
        return chunks

    def load(self):
        documents = []
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith(".txt"):
                    full_path = os.path.join(root, file)
                    text = self._read_file(full_path)
                    documents.extend(self._split_text(text))
        return documents
