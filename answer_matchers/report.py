"""Run a golden set through a provider and tabulate scores per matcher."""
import json
from collections import defaultdict
from pathlib import Path

from .matchers import score
from .provider import Provider

REQUIRED_KEYS = ("id", "expected", "matcher")


def load_golden(path: Path) -> list[dict[str, str]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        missing = [key for key in REQUIRED_KEYS if key not in row]
        if missing:
            raise ValueError(f"{path}:{number}: missing {missing}")
        rows.append(row)
    return rows


def evaluate(golden: list[dict[str, str]], provider: Provider) -> list[tuple[str, str, float]]:
    return [
        (row["id"], row["matcher"], score(row["matcher"], row["expected"], provider.complete(row["id"])))
        for row in golden
    ]


def format_report(results: list[tuple[str, str, float]], dataset: str) -> str:
    by_matcher: dict[str, list[float]] = defaultdict(list)
    lines = [f"{'case':<14}{'matcher':<13}score"]
    for case_id, matcher, value in results:
        by_matcher[matcher].append(value)
        lines.append(f"{case_id:<14}{matcher:<13}{value:.2f}")
    lines.append("")
    lines.append(f"{'matcher':<13}{'n':>3}  mean")
    for matcher in sorted(by_matcher):
        values = by_matcher[matcher]
        lines.append(f"{matcher:<13}{len(values):>3}  {sum(values) / len(values):.2f}")
    lines.append(f"\nfixture results: {len(results)} cases from {dataset}")
    return "\n".join(lines)
