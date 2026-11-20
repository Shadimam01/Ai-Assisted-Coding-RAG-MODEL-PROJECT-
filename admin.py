"""Admin panel: company documents and users."""
import streamlit as st

from config import SUPPORTED_EXTENSIONS
from core import auth
from core.ingest import (delete_company_file, ingest_company_docs, list_categories,
                         list_company_files, save_company_file)
from core.vectorstore import company_chunk_count
import ui


def _documents_tab():
    files = list_company_files()
    ui.stat_cards([
        (len(files), "Company files"),
        (len({f["category"] for f in files}), "Categories"),
        (company_chunk_count(), "Indexed chunks"),
    ])

    # ---- upload ----
    st.subheader("Add documents")
    st.session_state.setdefault("admin_upload_key", 0)
    cats = list_categories()
    NEW = "+ New category..."
    choice = st.selectbox("Category", cats + [NEW])
    category = choice
    if choice == NEW:
        category = st.text_input("New category name (for example: onboarding)")

    uploads = st.file_uploader(
        "Choose files",
        type=[e.strip(".") for e in SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
        key=f"admin_uploader_{st.session_state.admin_upload_key}",
    )
    if st.button("Save files", disabled=not uploads or not category):
        saved = 0
        for f in uploads:
            try:
                save_company_file(f.name, f.getvalue(), category)
                saved += 1
            except ValueError as e:
                st.error(str(e))
        if saved:
            st.session_state.admin_upload_key += 1
            st.session_state.admin_msg = f"Saved {saved} file(s). Click 'Rebuild knowledge base' to index them."
            st.rerun()

    if st.session_state.get("admin_msg"):
        st.success(st.session_state.pop("admin_msg"))

    # ---- rebuild ----
    st.subheader("Update the knowledge base")
    st.caption("After adding or deleting files, rebuild so the chatbot uses the latest documents.")
    if st.button("Rebuild knowledge base", type="primary"):
        with st.spinner("Reading and indexing all company documents..."):
            docs, chunks = ingest_company_docs()
        st.session_state.admin_msg = f"Indexed {docs} document(s) as {chunks} chunk(s). The chatbot is up to date."
        st.rerun()

    # ---- list / delete ----
    st.subheader("Current documents")
    if not files:
        st.info("No company documents yet. Add some above.")
        return
    st.dataframe(
        [{"Category": f["category"], "File": f["file"], "Size (KB)": f["size_kb"]} for f in files],
        use_container_width=True, hide_index=True,
    )
    labels = {f"{f['category']} / {f['file']}": f["path"] for f in files}
    with st.expander("Delete a document"):
        pick = st.selectbox("Choose a file", list(labels))
        sure = st.checkbox("Yes, delete this file")
        if st.button("Delete file", disabled=not sure):
            try:
                delete_company_file(labels[pick])
                st.session_state.admin_msg = f"Deleted {pick}. Rebuild the knowledge base to apply this."
                st.rerun()
            except Exception as e:
                st.error(f"Could not delete: {e}")


def _users_tab(current_user):
    users = auth.list_users()
    ui.stat_cards([
        (len(users), "Total users"),
        (sum(1 for u in users if u["role"] == "admin"), "Admins"),
        (sum(1 for u in users if u["role"] == "user"), "Normal users"),
    ])
    st.dataframe(
        [{"Username": u["username"], "Role": u["role"], "Created": u["created_at"]} for u in users],
        use_container_width=True, hide_index=True,
    )

    st.subheader("Add a user")
    with st.form("admin_add_user", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Username")
        pw = c2.text_input("Password", type="password")
        role = c3.selectbox("Role", list(auth.ROLES))
        if st.form_submit_button("Create user"):
            ok, msg = auth.create_user(name, pw, role)
            (st.success if ok else st.error)(msg)

    st.subheader("Manage an existing user")
    names = [u["username"] for u in users]
    target = st.selectbox("User", names)
    action = st.radio("Action", ["Change role", "Reset password", "Delete user"], horizontal=True)

    if action == "Change role":
        current = next(u["role"] for u in users if u["username"] == target)
        new_role = st.selectbox("New role", list(auth.ROLES), index=list(auth.ROLES).index(current))
        if st.button("Save role"):
            ok, msg = auth.set_role(target, new_role)
            (st.success if ok else st.error)(msg)
            if ok and target == current_user["username"]:
                st.session_state.user["role"] = new_role
                st.rerun()
    elif action == "Reset password":
        new_pw = st.text_input("New password", type="password")
        if st.button("Change password"):
            ok, msg = auth.reset_password(target, new_pw)
            (st.success if ok else st.error)(msg)
    else:
        if target == current_user["username"]:
            st.warning("You cannot delete the account you are logged in with.")
        else:
            sure = st.checkbox(f"Yes, delete {target}")
            if st.button("Delete user", disabled=not sure):
                ok, msg = auth.delete_user(target)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()


def admin_page(current_user):
    ui.admin_hero()
    tab_docs, tab_users = st.tabs(["Company documents", "Users"])
    with tab_docs:
        _documents_tab()
    with tab_users:
        _users_tab(current_user)
