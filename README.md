# Technical Documentation Assistant (RAG + LLM)

A chatbot for engineering teams, with login and an admin panel. It answers from pre-loaded company docs and can analyse
files you upload (PDF, DOCX, TXT, LOG, JSON).

## Setup

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install packages: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, choose `LLM_PROVIDER` and paste your API key.
5. Build the company knowledge base: `python -m scripts.ingest_company_docs`
6. Run the app: `streamlit run app.py`

The first run downloads the free embedding model (about 130 MB), so it takes a minute.

## Try it

- Source: Company Docs, ask: "What is our naming convention for REST endpoints?"
- Upload `samples/sample_error.log`, click "Explain this error" or "Suggest a fix".

## Add your own company docs

Put files in `data/company_docs/<category>/` (for example `api`, `standards`, `runbooks`),
then click "Rebuild knowledge base" in the sidebar, or re-run step 5.

## Login and admin panel

- The first time the app runs it creates an admin account from `.env`
  (`ADMIN_USERNAME` / `ADMIN_PASSWORD`, default `admin` / `admin123`). Change the password in `.env`
  BEFORE the first run, or change it later in the Admin Panel > Users.
- New people can create a normal "user" account from the Sign up tab
  (set `ALLOW_SIGNUP=false` in `.env` to turn this off).
- Users can chat and upload files. Only admins see the **Admin Panel**, where they can:
  - add or delete company documents and rebuild the knowledge base
  - create users, change roles, reset passwords and delete users
- Accounts are stored in `data/users.db` (passwords are saved as salted hashes, never as plain text).
