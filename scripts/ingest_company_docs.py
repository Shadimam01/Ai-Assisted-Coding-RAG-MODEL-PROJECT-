"""Run once (and again whenever company docs change):  python -m scripts.ingest_company_docs"""
from core.ingest import ingest_company_docs

if __name__ == "__main__":
    docs, chunks = ingest_company_docs()
    print(f"Indexed {docs} document(s) as {chunks} chunk(s).")
