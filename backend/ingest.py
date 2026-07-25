import os

from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from settings import Settings
from documents import load_documents, chunk_documents
from vector_database import VectorDatabase

raw_docs = load_documents(path=Settings.DOCS_PATH)
print(f"{len(raw_docs)} documents found")

ids, docs, metadatas = chunk_documents(
    doc_contents=raw_docs, chunk_size=Settings.CHUNK_SIZE, chunk_overlap=Settings.CHUNK_OVERLAP)
print(f"{len(ids)} chunks generated")

vector_database = VectorDatabase.build_from_settings(settings=Settings)

print("Writing documents")
vector_database.insert(ids=ids, docs=docs, metadatas=metadatas)

print("Ready")
