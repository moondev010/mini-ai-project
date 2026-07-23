import os
import uuid

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def load_documents(path: str) -> list[str]:
    doc_paths = []
    doc_contents = []

    for dirpath, _dirnames, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                doc_paths.append(f"{dirpath}/{file}")

    for doc_path in doc_paths:
        with open(doc_path, "r") as doc_file:
            doc_contents.append(doc_file.read())

    return doc_contents


def chunk_documents(doc_contents: list[str], chunk_size: int, chunk_overlap: int, generate_ids: bool = True):
    ids, docs, metadatas = [], [], []

    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2")
    ]

    separators = ["\n\n", "\n", ". ", "! ", "? ", "¡", "¿", " ", ""]

    split_head = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )

    split_text = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )

    for content in doc_contents:
        head_chunks = split_head.split_text(content)

        final_chunks = split_text.split_documents(head_chunks)

        for chunk in final_chunks:
            if generate_ids:
                ids.append(str(uuid.uuid4()))

            prefix = build_header_prefix(chunk.metadata)

            docs.append(f"{prefix}\n{chunk.page_content}")
            metadatas.append(chunk.metadata)

    if generate_ids:
        return ids, docs, metadatas
    else:
        return docs, metadatas


def build_header_prefix(metadata: dict):
    parts = []

    for k in metadata.keys():
        if k in ("h1", "h2", "h3"):
            parts.append(metadata[k])

    return " > ".join(parts)
