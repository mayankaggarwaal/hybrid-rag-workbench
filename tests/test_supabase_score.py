from pathlib import Path


def test_supabase_rrf_score_is_normalized_for_service_threshold() -> None:
    source = Path("app/retrieval/supabase.py").read_text(encoding="utf-8")
    assert "30.0 * (COALESCE(1.0/(60+l.rank),0)" in source

