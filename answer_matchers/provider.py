"""Provider seam: every model call goes through `complete`."""
import json
from pathlib import Path
from typing import Protocol


class Provider(Protocol):
    def complete(self, case_id: str) -> str: ...


class ReplayProvider:
    """Replays recorded answers so the eval runs offline and deterministically."""

    def __init__(self, answers: dict[str, str]) -> None:
        self._answers = answers

    @classmethod
    def from_jsonl(cls, path: Path) -> "ReplayProvider":
        answers: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                answers[row["id"]] = row["answer"]
        return cls(answers)

    def complete(self, case_id: str) -> str:
        if case_id not in self._answers:
            raise KeyError(f"no recorded answer for case {case_id!r}")
        return self._answers[case_id]
