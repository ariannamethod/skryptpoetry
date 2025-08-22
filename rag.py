from pathlib import Path
from typing import Iterable

from skryptmetrics import resonance


def retrieve(query: str, documents: Iterable[Path]) -> str:
    """Return the content of the document that resonates most with query."""
    best_text = ""
    best_score = -1.0
    for path in documents:
        try:
            text = Path(path).read_text(encoding='utf-8')
        except FileNotFoundError:
            continue
        score = resonance(query, text)
        if score > best_score:
            best_score = score
            best_text = text
    return best_text
