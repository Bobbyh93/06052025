from dataclasses import dataclass
import os
from typing import Dict


def _read_env_file(path: str) -> Dict[str, str]:
    """Simple .env reader used when python-dotenv is unavailable."""
    data: Dict[str, str] = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                data[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return data

@dataclass
class Config:
    docs_path: str
    embeddings_model: str
    index_path: str
    openai_api_key: str
    chunk_size: int
    chunk_overlap: int
    persist_index: bool
    top_k: int
    llm_model: str

    @classmethod
    def load(cls, env_path: str = '.env') -> 'Config':
        env = _read_env_file(env_path)
        os.environ.update({k: v for k, v in env.items() if k not in os.environ})
        return cls(
            docs_path=os.getenv('DOCS_PATH', './data'),
            embeddings_model=os.getenv('EMBEDDINGS_MODEL', ''),
            index_path=os.getenv('INDEX_PATH', './faiss_index'),
            openai_api_key=os.getenv('OPENAI_API_KEY', ''),
            chunk_size=int(os.getenv('CHUNK_SIZE', '512')),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', '50')),
            persist_index=os.getenv('PERSIST_INDEX', 'true').lower() == 'true',
            top_k=int(os.getenv('TOP_K', '5')),
            llm_model=os.getenv('LLM_MODEL', 'gpt-3.5-turbo'),
        )
