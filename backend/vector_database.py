from chromadb import ClientAPI, Collection, EmbeddingFunction


class VectorDatabase:
    _chroma_client: ClientAPI
    _collection: Collection

    def __init__(self, chroma_client: ClientAPI, collection_name: str, embedding_function: EmbeddingFunction):
        self._chroma_client = chroma_client

        self._collection = self._chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def insert(self, ids: list[str], documents: list[str], metadatas: dict[any, any]):
        self._collection.add(ids=ids, documents=documents, metadatas=metadatas)
        

