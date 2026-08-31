"""Make one synthetic-only Gemini request without printing credentials or response content."""

from app.config import get_settings
from app.llm import GeminiProvider


def main() -> None:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise SystemExit("Gemini smoke check skipped: GEMINI_API_KEY is not configured")

    provider = GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    response = provider.generate(
        "State only the recorded synthetic primary deployment window with its evidence label.",
        ["[E1] Synthetic record: primary deployment window is 30 minutes."],
    )
    if not response.strip():
        raise SystemExit("Gemini smoke check failed: empty response")
    print("Gemini smoke check succeeded with a non-empty synthetic-only response")


if __name__ == "__main__":
    main()

