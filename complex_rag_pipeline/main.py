from rag_pipeline.config import Config
from rag_pipeline.loader import DocumentLoader
from rag_pipeline.embedder import SimpleEmbedder
from rag_pipeline.index import SimpleIndex
from rag_pipeline.retriever import Retriever
from rag_pipeline.llm import DummyLLM
from rag_pipeline.rag import RAGPipeline


def main():
    config = Config.load()
    loader = DocumentLoader(config.docs_path, config.chunk_size, config.chunk_overlap)
    embedder = SimpleEmbedder()
    index = SimpleIndex(dim=26, index_path=config.index_path, persist=config.persist_index)
    retriever = Retriever(index, embedder, config.top_k)
    llm = DummyLLM(config.llm_model, config.openai_api_key)

    rag = RAGPipeline(loader, embedder, index, retriever, llm)
    rag.build()

    question = input("Ask a question: ")
    answer = rag.query(question)
    print(answer)

if __name__ == "__main__":
    main()
