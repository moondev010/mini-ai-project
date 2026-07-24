import os

from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from settings import Settings
from documents import load_documents, chunk_documents
from vector_database import VectorDatabase

load_dotenv()

client = PersistentClient(path=Settings.CHROMADB_PATH)
ollama_fn = OllamaEmbeddingFunction(model_name=Settings.EMBEDDING_MODEL)

raw_docs = load_documents(Settings.DOCS_PATH)
print(f"{len(raw_docs)} documents found")

ids, docs, metadatas = chunk_documents(
    raw_docs, Settings.CHUNK_SIZE, Settings.CHUNK_OVERLAP)
print(f"{len(ids)} chunks generated")

vector_database = VectorDatabase(client, Settings.COLLECTION, ollama_fn)

print("Writing documents")
vector_database.insert(ids, docs, metadatas)

print("Ready")
