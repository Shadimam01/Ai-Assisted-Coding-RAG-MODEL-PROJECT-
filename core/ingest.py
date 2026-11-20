"""Manage the company documents folder and load it into the knowledge base."""
import re
from pathlib import Path

from config import COMPANY_DOCS_DIR, SUPPORTED_EXTENSIONS
from core.loader import load_file, split_documents
from core.vectorstore import reset_company_store


def _category_of(path):
    return path.parent.name if path.parent != COMPANY_DOCS_DIR else "general"


def safe_category(name):
    """Keep category names simple so they are safe folder names."""
    return re.sub(r"[^A-Za-z0-9_-]", "_", (name or "").strip()) or "general"


def ingest_company_docs():
    """Returns (number_of_documents, number_of_chunks)."""
    docs = []
    for path in sorted(COMPANY_DOCS_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        # The sub-folder name becomes the category: api / standards / runbooks
        for d in load_file(path):
            d.metadata["category"] = _category_of(path)
            docs.append(d)

    if not docs:
        return 0, 0

    chunks = split_documents(docs)
    store = reset_company_store()
    store.add_documents(chunks)
    return len(docs), len(chunks)


def list_categories():
    COMPANY_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    cats = {p.name for p in COMPANY_DOCS_DIR.iterdir() if p.is_dir()}
    return sorted(cats) or ["general"]


def list_company_files():
    """All company files as a list of dicts (category, file, size_kb, path)."""
    COMPANY_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for path in sorted(COMPANY_DOCS_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            out.append({
                "category": _category_of(path),
                "file": path.name,
                "size_kb": round(path.stat().st_size / 1024, 1),
                "path": str(path),
            })
    return out


def save_company_file(filename, data, category):
    """Save an uploaded file into data/company_docs/<category>/. Returns (category, filename)."""
    name = Path(filename).name
    if Path(name).suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {name}")
    cat = safe_category(category)
    folder = COMPANY_DOCS_DIR / cat
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(data)
    return cat, name


def delete_company_file(path):
    """Delete one company file (only files inside the company docs folder)."""
    target = Path(path).resolve()
    if COMPANY_DOCS_DIR.resolve() not in target.parents:
        raise ValueError("Invalid file path.")
    target.unlink()
