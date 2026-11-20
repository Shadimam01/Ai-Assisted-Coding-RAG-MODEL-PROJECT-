"""Retrieval + answer generation."""
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from core.llm import get_llm
from core.prompts import SYSTEM_PROMPT, USER_TEMPLATE
from core.vectorstore import get_company_store


def retrieve(question, mode, upload_store=None, categories=None, k=4):
    """Search the chosen source(s). Returns a list of (label, Document)."""
    results = []

    if mode in ("Company Docs", "Both"):
        flt = {"category": {"$in": categories}} if categories else None
        for d in get_company_store().similarity_search(question, k=k, filter=flt):
            results.append(("COMPANY", d))

    if mode in ("My Upload", "Both") and upload_store is not None:
        for d in upload_store.similarity_search(question, k=k):
            results.append(("UPLOAD", d))

    return results


def format_context(results):
    if not results:
        return "(no relevant text found)"
    blocks = []
    for label, d in results:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "-")
        blocks.append(f"[{label} | {src} | page {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)


def stream_answer(question, history, results, log_summary=""):
    """Yield the answer piece by piece. `history` = earlier messages (without this question)."""
    llm = get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in history[-6:]:
        cls = HumanMessage if m["role"] == "user" else AIMessage
        messages.append(cls(content=m["content"]))

    extra = ""
    if log_summary:
        extra = f"KEY LINES FROM THE UPLOADED LOG (errors and stack traces):\n{log_summary}\n\n"

    messages.append(HumanMessage(content=USER_TEMPLATE.format(
        extra=extra, context=format_context(results), question=question)))

    for chunk in llm.stream(messages):
        text = chunk.content
        if isinstance(text, list):
            text = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in text)
        if text:
            yield text
