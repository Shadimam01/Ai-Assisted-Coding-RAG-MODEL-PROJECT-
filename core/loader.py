"""Read files (PDF, DOCX, text, logs) and split them into chunks."""
import re
from pathlib import Path

import docx
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config import CHUNK_OVERLAP, CHUNK_SIZE, SUPPORTED_EXTENSIONS


def load_file(path, source_name=None):
    """Return a list of Documents (one per PDF page, or one per file)."""
    path = Path(path)
    ext = path.suffix.lower()
    name = source_name or path.name

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        reader = PdfReader(str(path))
        docs = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                docs.append(Document(page_content=text, metadata={"source": name, "page": i}))
        return docs

    if ext == ".docx":
        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs if p.text.strip()]
        for table in d.tables:
            for row in table.rows:
                parts.append(" | ".join(c.text.strip() for c in row.cells))
        text = "\n".join(parts)
        return [Document(page_content=text, metadata={"source": name, "page": 1})] if text.strip() else []

    text = path.read_text(encoding="utf-8", errors="ignore")
    return [Document(page_content=text, metadata={"source": name, "page": 1})] if text.strip() else []


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(docs)


ERROR_PATTERN = re.compile(
    r"(ERROR|FATAL|CRITICAL|Exception|Error|Traceback|Caused by|\bat\s+[\w.$]+\()"
)


def extract_error_lines(text, max_lines=60):
    """Pull out error lines, stack traces and a little context from a log."""
    lines = text.splitlines()
    keep = set()
    for i, line in enumerate(lines):
        if ERROR_PATTERN.search(line):
            for j in range(max(0, i - 1), min(len(lines), i + 3)):
                keep.add(j)
    selected = [lines[i] for i in sorted(keep)]
    return "\n".join(selected[:max_lines])
