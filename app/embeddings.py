import hashlib
import math
import re


def hash_embedding(text: str, dimensions: int = 384) -> list[float]:
    """Deterministic local embedding for demos/tests; replace in production."""
    values = [0.0] * dimensions
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        digest = hashlib.sha256(token.encode()).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        values[index] += 1.0 if digest[4] % 2 else -1.0
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return [value / norm for value in values]

