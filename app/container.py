from pathlib import Path

from app.config import get_settings
from app.ingest import load_bundle, normalize_bundle
from app.llm import GeminiProvider, GroqProvider, MockProvider
from app.retrieval.memory import InMemoryRetrievalProvider
from app.retrieval.supabase import SupabasePostgresProvider
from app.service import RAGService


def build_service() -> RAGService:
    settings = get_settings()
    if settings.supabase_db_url:
        retrieval = SupabasePostgresProvider(settings.supabase_db_url, settings.embedding_dimension)
    else:
        retrieval = InMemoryRetrievalProvider(settings.embedding_dimension)
        path = Path(__file__).parent.parent / "data" / "synthetic_bundle.json"
        retrieval.index(normalize_bundle(load_bundle(path), settings.embedding_dimension))
    provider_name = settings.llm_provider.lower()
    if provider_name == "groq":
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
        llm = GroqProvider(settings.groq_api_key, settings.groq_model)
    elif provider_name == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        llm = GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    else:
        llm = MockProvider()
    return RAGService(retrieval, llm, settings.top_k)
