"""Vector databases: a permanent one for company docs, a temporary one per upload session."""
import uuid
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_DIR, COMPANY_COLLECTION, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, encode_kwargs={"normalize_embeddings": True})


def get_company_store():
    """Persistent store for the pre-loaded company knowledge base."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COMPANY_COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def reset_company_store():
    """Delete the old company collection and return a fresh empty one."""
    store = get_company_store()
    try:
        store.delete_collection()
    except Exception:
        pass
    return get_company_store()


def company_store_has_data():
    try:
        return len(get_company_store().get(limit=1)["ids"]) > 0
    except Exception:
        return False


def new_upload_store():
    """Temporary in-memory store for the current user's uploads."""
    return Chroma(
        collection_name=f"upload_{uuid.uuid4().hex[:12]}",
        embedding_function=get_embeddings(),
    )


def company_chunk_count():
    try:
        return len(get_company_store().get(include=[])["ids"])
    except Exception:
        return 0
