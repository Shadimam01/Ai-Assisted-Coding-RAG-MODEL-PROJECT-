import os
import tempfile
from pathlib import Path

import streamlit as st

from config import LLM_PROVIDER, SUPPORTED_EXTENSIONS, TOP_K
from core.auth import init_db
from core.ingest import list_categories
from core.loader import extract_error_lines, load_file, split_documents
from core.prompts import QUICK_ACTIONS
from core.rag import retrieve, stream_answer
from core.vectorstore import company_store_has_data, new_upload_store
import admin
import auth_ui
import ui

st.set_page_config(page_title="Tech Doc Assistant", page_icon="📘", layout="wide")
ui.inject_css()


# ---------- session state ----------
def init_state():
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("upload_store", None)
    st.session_state.setdefault("processed_files", set())
    st.session_state.setdefault("uploaded_names", [])
    st.session_state.setdefault("log_summary", "")


def process_upload(uploaded):
    """Parse one uploaded file and add it to the temporary upload store."""
    suffix = Path(uploaded.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name
    try:
        docs = load_file(tmp_path, source_name=uploaded.name)
    finally:
        os.unlink(tmp_path)

    if not docs:
        return 0

    if suffix == ".log":
        full_text = "\n".join(d.page_content for d in docs)
        summary = extract_error_lines(full_text)
        if summary:
            st.session_state.log_summary += f"\n# {uploaded.name}\n{summary}\n"

    chunks = split_documents(docs)
    if st.session_state.upload_store is None:
        st.session_state.upload_store = new_upload_store()
    st.session_state.upload_store.add_documents(chunks)
    return len(chunks)


def clear_uploads():
    st.session_state.upload_store = None
    st.session_state.processed_files = set()
    st.session_state.uploaded_names = []
    st.session_state.log_summary = ""


def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def show_sources(results):
    if not results:
        return
    with st.expander(f"Sources used ({len(results)})"):
        for label, d in results:
            src = d.metadata.get("source", "unknown")
            page = d.metadata.get("page", "-")
            cat = d.metadata.get("category", "")
            tag = f"{label} · {src} · page {page}" + (f" · {cat}" if cat else "")
            st.markdown(f"**{tag}**")
            snippet = d.page_content.strip().replace("\n", " ")
            st.caption(snippet[:350] + ("..." if len(snippet) > 350 else ""))


init_state()
init_db()

# ---------- login gate ----------
if st.session_state.user is None:
    auth_ui.login_screen()
    st.stop()

user = st.session_state.user
is_admin = user["role"] == "admin"

# ---------- sidebar ----------
page = "Chat"
mode, categories, top_k = "Both", None, TOP_K
with st.sidebar:
    ui.sidebar_brand()
    ui.user_badge(user["username"], user["role"])
    if is_admin:
        page = st.radio("Go to", ["Chat", "Admin Panel"], horizontal=True)
    if st.button("Logout", use_container_width=True):
        logout()
    st.divider()

    if page == "Chat":
        mode = st.radio("Knowledge source", ["Company Docs", "My Upload", "Both"], index=2)

        if mode in ("Company Docs", "Both"):
            all_cats = list_categories()
            picked = st.multiselect("Filter company docs", all_cats, default=all_cats)
            categories = picked or None

        st.divider()
        st.subheader("Upload a file")
        files = st.file_uploader(
            "PDF, DOCX, TXT, LOG, JSON",
            type=[e.strip(".") for e in SUPPORTED_EXTENSIONS],
            accept_multiple_files=True,
        )
        for f in files or []:
            key = (f.name, f.size)
            if key not in st.session_state.processed_files:
                with st.spinner(f"Reading {f.name}..."):
                    n = process_upload(f)
                st.session_state.processed_files.add(key)
                if n:
                    st.session_state.uploaded_names.append(f.name)
                else:
                    st.warning(f"No readable text found in {f.name}.")

        if st.session_state.uploaded_names:
            st.success("Loaded: " + ", ".join(st.session_state.uploaded_names))
            if st.button("Remove uploaded files"):
                clear_uploads()
                st.rerun()

        st.divider()
        top_k = st.slider("Chunks per search", 2, 10, TOP_K)
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

# ---------- admin page ----------
if page == "Admin Panel":
    admin.admin_page(user)
    st.stop()

# ---------- main area ----------
ui.hero()
kb_ready = company_store_has_data()
ui.chips(LLM_PROVIDER, mode, len(st.session_state.uploaded_names), kb_ready)

if mode in ("Company Docs", "Both") and not kb_ready:
    if is_admin:
        st.warning("The company knowledge base is empty. Open the Admin Panel and click 'Rebuild knowledge base'.")
    else:
        st.warning("The company knowledge base is empty. Please ask an admin to set it up.")

# quick action buttons
action = None
prompt = None
ICONS = {"Explain this error": "🐞", "Suggest a fix": "🛠️",
         "Summarize this spec": "📄", "Check against coding standards": "✅"}
cols = st.columns(len(QUICK_ACTIONS))
for col, (label, spec) in zip(cols, QUICK_ACTIONS.items()):
    if col.button(f"{ICONS.get(label, '')} {label}", use_container_width=True):
        action = spec
        prompt = spec[0]

# chat history
if not st.session_state.messages:
    ui.welcome()
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            show_sources(m["sources"])

typed = st.chat_input("Ask a question...")
if typed:
    prompt = typed
    action = None

# ---------- handle a new question ----------
if prompt:
    active_mode = mode
    active_k = top_k
    if action:
        _, forced_mode, active_k = action
        active_mode = forced_mode or mode

    history = list(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        needs_upload = active_mode in ("My Upload",) or (action and "uploaded file" in prompt)
        if needs_upload and st.session_state.upload_store is None:
            msg = "Please upload a file first (sidebar), then ask again."
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            try:
                with st.spinner("Searching documents..."):
                    results = retrieve(
                        prompt, active_mode,
                        upload_store=st.session_state.upload_store,
                        categories=categories, k=active_k,
                    )
                answer = st.write_stream(
                    stream_answer(prompt, history, results, st.session_state.log_summary)
                )
                show_sources(results)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": results}
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
