from typing import Any

from chromadb import ClientAPI, Collection, EmbeddingFunction, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from settings import Settings


def log_search_results(results: dict[str, Any]) -> None:
    headers = [metadata.get("h1", "") for metadata in results["metadatas"][0]]
    distances = results["distances"][0]

    for header, distance in zip(headers, distances):
        print(f"Header: {header} | Distance: {distance}")

    print("-----------------------")


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

        log_search_results(results)

        for i, rank in enumerate(results["distances"][0]):
            if rank <= threshold:
                filtered_docs.append(results["documents"][0][i])

        return filtered_docs


def build_final_prompt(system_prompt: str, user_chunks: list[str], assistant_chunks: list[str]) -> str:

    final_prompt = ""

    if len(user_chunks) > 0:
        joined_user_chunks = "\n\n".join(user_chunks)
        final_prompt += f"{system_prompt}\n# RELEVANT USER CHUNKS\n{joined_user_chunks}"

    if len(assistant_chunks) > 0:
        joined_assistant_chunks = "\n\n".join(assistant_chunks)
        final_prompt += f"{system_prompt}\n# RELEVANT ASSISTANT CHUNKS\n{joined_assistant_chunks}"

    if not (len(user_chunks) > 0 and len(assistant_chunks) > 0):
        final_prompt = system_prompt

    return final_prompt
