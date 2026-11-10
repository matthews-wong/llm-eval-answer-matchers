"""Answer matchers. Each takes (expected, answer) and returns a score in [0, 1]."""
import json
import re
from collections import Counter
from typing import Callable

from .normalize import normalize, tokens

DEFAULT_REL_TOL = 0.01
_NUMBER = re.compile(r"-?\d[\d,]*\.?\d*")

Matcher = Callable[[str, str], float]


def exact(expected: str, answer: str) -> float:
    return float(expected == answer)


def normalized(expected: str, answer: str) -> float:
    return float(normalize(expected) == normalize(answer))


def token_f1(expected: str, answer: str) -> float:
    want, got = tokens(expected), tokens(answer)
    if not want or not got:
        return float(want == got)
    overlap = sum((Counter(want) & Counter(got)).values())
    if overlap == 0:
        return 0.0
    precision, recall = overlap / len(got), overlap / len(want)
    return 2 * precision * recall / (precision + recall)


def _first_number(text: str) -> float | None:
    match = _NUMBER.search(text)
    if match is None:
        return None
    try:
        return float(match.group().replace(",", "").rstrip("."))
    except ValueError:
        return None


def numeric(expected: str, answer: str, rel_tol: float = DEFAULT_REL_TOL) -> float:
    want, got = _first_number(expected), _first_number(answer)
    if want is None:
        raise ValueError(f"expected value has no number: {expected!r}")
    if got is None:
        return 0.0
    return float(abs(want - got) <= rel_tol * abs(want))


def json_fields(expected: str, answer: str) -> float:
    want = json.loads(expected)
    if not isinstance(want, dict):
        raise ValueError(f"expected value must be a JSON object: {expected!r}")
    try:
        got = json.loads(answer)
    except json.JSONDecodeError:
        return 0.0
    if not isinstance(got, dict):
        return 0.0
    return float(all(key in got and got[key] == value for key, value in want.items()))


MATCHERS: dict[str, Matcher] = {
    "exact": exact,
    "normalized": normalized,
    "token_f1": token_f1,
    "numeric": numeric,
    "json_fields": json_fields,
}


def score(name: str, expected: str, answer: str) -> float:
    if name not in MATCHERS:
        raise KeyError(f"unknown matcher {name!r}; choose from {sorted(MATCHERS)}")
    return MATCHERS[name](expected, answer)
