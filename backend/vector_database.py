from typing import Any

from chromadb import ClientAPI, Collection, EmbeddingFunction, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from settings import Settings


class VectorDatabase:
    _chroma_client: ClientAPI
    _collection: Collection

    def __init__(self, chroma_client: ClientAPI, embedding_function: EmbeddingFunction, collection_name: str):
        self._chroma_client = chroma_client

        self._collection = self._chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            configuration={"hnsw": {"space": "cosine"}}
        )

    @classmethod
    def build_from_settings(cls, settings: Settings) -> "VectorDatabase":
        client = PersistentClient(path=settings.CHROMADB_PATH)
        ollama_ef = OllamaEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL)

        return cls(
            chroma_client=client,
            embedding_function=ollama_ef,
            collection_name=settings.COLLECTION
        )

    def insert(self, ids: list[str], docs: list[str], metadatas: list[dict[str, Any]]):
        self._collection.add(ids=ids, documents=docs, metadatas=metadatas)

    def search(self, prompt: str, k: int = 5, threshold: float = 0.54) -> list[str]:
        filtered_docs = []

        results = self._collection.query(query_texts=[prompt], n_results=k)

        for i, rank in enumerate(results["distances"][0]):
            if rank <= threshold:
                filtered_docs.append(results["documents"][0][i])

        # print(results["documents"])
        # print(results["distances"][0])

        return filtered_docs


def build_final_prompt(system_prompt: str, chunks: list[str]):
    joined_chunks = "\n\n".join(chunks)

    return f"{system_prompt}\n# RELEVANT CHUNKS\n{joined_chunks}"
