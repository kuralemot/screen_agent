import uuid
from datetime import datetime
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from config import settings

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        _collection = _client.get_or_create_collection(
            name=settings.chroma_collection, embedding_function=embed_fn
        )
    return _collection


def add_observation(description: str, screenshot_path: Optional[str] = None) -> str:
    obs_id = str(uuid.uuid4())
    metadata = {"timestamp": datetime.now().isoformat()}
    if screenshot_path:
        metadata["screenshot_path"] = str(screenshot_path)
    _get_collection().add(ids=[obs_id], documents=[description], metadatas=[metadata])
    return obs_id


def query(text: str, n_results: int = 5):
    result = _get_collection().query(query_texts=[text], n_results=n_results)
    matches = []
    for doc, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        matches.append({"description": doc, "metadata": meta, "distance": dist})
    return matches
