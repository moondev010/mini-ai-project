import os

from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from documents import load_documents, chunk_documents
from vector_database import VectorDatabase

load_dotenv()

CHROMADB_PATH = os.getenv("CHROMADB_PATH", "chroma_data")
COLLECTION = os.getenv("COLLECTION", "docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embeddinggemma")
DOCS_PATH = os.getenv("DOCS_PATH", "docs")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "384"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "40"))

client = PersistentClient(path=CHROMADB_PATH)
ollama_fn = OllamaEmbeddingFunction(model_name=EMBEDDING_MODEL)

raw_docs = load_documents(DOCS_PATH)
print(f"{len(raw_docs)} documents found")

ids, docs, metadatas = chunk_documents(raw_docs, CHUNK_SIZE, CHUNK_OVERLAP)
print(f"{len(ids)} chunks generated")

vector_database = VectorDatabase(client, COLLECTION, ollama_fn)

print("Writing documents")
vector_database.insert(ids, docs, metadatas)

print("Ready")
