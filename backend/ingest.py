import os

from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from settings import Settings
from documents import load_documents, chunk_documents
from vector_database import VectorDatabase

load_dotenv()

settings = Settings()

client = PersistentClient(path=settings.CHROMADB_PATH)
ollama_fn = OllamaEmbeddingFunction(model_name=settings.EMBEDDING_MODEL)

raw_docs = load_documents(settings.DOCS_PATH)
print(f"{len(raw_docs)} documents found")

ids, docs, metadatas = chunk_documents(
    raw_docs, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
print(f"{len(ids)} chunks generated")

vector_database = VectorDatabase(client, settings.COLLECTION, ollama_fn)

print("Writing documents")
vector_database.insert(ids, docs, metadatas)

print("Ready")
