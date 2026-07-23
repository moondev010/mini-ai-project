from chromadb import ClientAPI, Collection, EmbeddingFunction


class VectorDatabase:
    _chroma_client: ClientAPI
    _collection: Collection

    def __init__(self, chroma_client: ClientAPI, collection_name: str, embedding_function: EmbeddingFunction):
        self._chroma_client = chroma_client

        self._collection = self._chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            configuration={"hnsw": {"space": "cosine"}}
        )

    def insert(self, ids: list[str], documents: list[str], metadatas: dict[any, any]):
        self._collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def search(self, prompt: str, k: int, threshold: float = 0.8):
        filtered_docs = []

        results = self._collection.query(query_texts=[prompt], n_results=k)

        for i, rank in enumerate(results["distances"][0]):
            if rank <= threshold:
                # print("Threshold")
                filtered_docs.append(results["documents"][0][i])

        # print(results["documents"])
        print(results["distances"][0])

        return filtered_docs
