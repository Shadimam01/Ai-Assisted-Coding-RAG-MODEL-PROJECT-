SYSTEM_PROMPT = """You are a Technical Documentation Assistant for an engineering team.

Rules:
1. Answer ONLY using the provided context (company documents and/or the user's uploaded file).
2. If the context does not contain the answer, say: "I couldn't find this in the available documents." Do not guess.
3. Mention the source after each key point, like [Source: file name, page].
4. Put code, commands and config in fenced code blocks.
5. Be clear and concise. Use short steps when explaining a fix.
6. Text marked COMPANY comes from official company docs. Text marked UPLOAD comes from the user's own file."""

USER_TEMPLATE = """{extra}CONTEXT:
{context}

QUESTION:
{question}"""

# label -> (prompt, force_source_mode, number_of_chunks)
QUICK_ACTIONS = {
    "Explain this error": (
        "Explain the error in my uploaded file: what happened, the likely root cause, and what to check first.",
        None, 4),
    "Suggest a fix": (
        "Suggest a step-by-step fix for the problem in my uploaded file, using the company runbooks and API docs.",
        "Both", 5),
    "Summarize this spec": (
        "Summarize my uploaded file: its purpose, key points and any requirements.",
        "My Upload", 8),
    "Check against coding standards": (
        "Check my uploaded file against the company coding standards. List each violation with the rule it breaks and how to correct it.",
        "Both", 6),
}
