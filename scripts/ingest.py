import argparse

from app.config import get_settings
from app.ingest import load_bundle, normalize_bundle
from app.retrieval.supabase import SupabasePostgresProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize synthetic source JSON and index in Supabase")
    parser.add_argument("path", nargs="?", default="data/synthetic_bundle.json")
    args = parser.parse_args()
    settings = get_settings()
    if not settings.supabase_db_url:
        raise SystemExit("Set SUPABASE_DB_URL. No database has been modified.")
    documents = normalize_bundle(load_bundle(args.path), settings.embedding_dimension)
    SupabasePostgresProvider(settings.supabase_db_url, settings.embedding_dimension).index(documents)
    print(f"Indexed {len(documents)} synthetic documents")


if __name__ == "__main__":
    main()


