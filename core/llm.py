"""Pick the LLM from the .env file. Swapping providers needs no other code change."""
from config import (GEMINI_MODEL, GOOGLE_API_KEY, GROQ_API_KEY, GROQ_MODEL,
                    LLM_PROVIDER, OLLAMA_MODEL)


def get_llm():
    if LLM_PROVIDER == "gemini":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
        from langchain_groq import ChatGroq
        return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=OLLAMA_MODEL, temperature=0.2)

    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")
