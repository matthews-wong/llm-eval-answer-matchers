import sys
from pathlib import Path

from .provider import ReplayProvider
from .report import evaluate, format_report, load_golden

USAGE = "usage: python3 -m answer_matchers GOLDEN.jsonl ANSWERS.jsonl"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    golden_path, answers_path = Path(argv[0]), Path(argv[1])
    results = evaluate(load_golden(golden_path), ReplayProvider.from_jsonl(answers_path))
    print(format_report(results, golden_path.name))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
