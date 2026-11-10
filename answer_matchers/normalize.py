"""Text folding shared by the matchers."""
import re
import string
import unicodedata

_ARTICLES = re.compile(r"\b(a|an|the)\b")
_PUNCTUATION = set(string.punctuation)


def normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text).lower()
    folded = "".join(ch for ch in folded if ch not in _PUNCTUATION)
    folded = _ARTICLES.sub(" ", folded)
    return " ".join(folded.split())


def tokens(text: str) -> list[str]:
    return normalize(text).split()
