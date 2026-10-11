"""
Load a document -> split it into chunks -> embed the chunks -> store them in Pinecone.

Used by both data_ingestion.py (bulk load of ./documents) and POST /api/upload,
so documents are always processed the same way.
"""

from pathlib import Path
from typing import List
from hashlib import sha256
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx import Document as DocxDocument
from src.config import get_settings
from src.vectorstore import get_vector_store

SUPPORTED = {".pdf", ".txt", ".md", ".docx"}


def __load_docx(path: Path) -> List[Document]:
    doc = DocxDocument(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [
        Document(page_content=text, metadata={"source": str(path), "title": path.name})
    ]


# Turn a file into LangChain Document objects (text + metadata such as title/page).
def load_file(path: Path) -> List[Document]:
    ext = path.suffix.lower()
    if ext == ".pdf":
        docs = PyPDFLoader(file_path=path).load()  # one Document per PDF page
    elif ext in {".txt", ".md"}:
        docs = TextLoader(str(path), encoding="utf-8").load()
    elif ext == ".docx":
        docs = __load_docx(path)
    else:
        raise ValueError(f"Unsupported file type :{ext}. Use PDF,txt,md or docx ")

    for d in docs:
        d.metadata.setdefault("source", str(path))
        d.metadata.setdefault("title", path.name)
        d.metadata["document_name"] = path.name
    return docs


def _stable_chunk_id(path: Path, chunk: Document, position: int) -> str:
    """Stable IDs make repeat ingestion idempotent instead of creating duplicates."""
    material = f"{path.name}|{position}|{chunk.page_content}".encode("utf-8")
    digest = sha256(material).hexdigest()[:24]
    safe_stem = "".join(c if c.isalnum() or c in "-_" else "-" for c in path.stem)[:60]
    return f"{safe_stem}-{position}-{digest}"


# Returns the number of chunks stored in Pinecone.
def ingest_file(path: Path) -> int:
    docs = load_file(path)
    # ~800-character chunks with 160 characters of overlap, so a sentence cut at a
    # chunk boundary still appears whole in one of the two neighbouring chunks.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=160, separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    if not chunks:
        return 0

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["knowledge_base"] = get_settings().pinecone_namespace

    ids = [_stable_chunk_id(path, chunk, i) for i, chunk in enumerate(chunks)]
    # add_documents embeds each chunk with OpenAI and upserts it into Pinecone.
    get_vector_store().add_documents(chunks, ids=ids)
    return len(chunks)


def ingest_directory(directory: Path) -> int:
    total = 0
    if not directory.exists():
        return 0
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED:
            total += ingest_file(path)
    return total


def namespace() -> str:
    return get_settings().pinecone_namespace
