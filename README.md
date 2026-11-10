# llm-eval-answer-matchers

Small, deterministic matchers for scoring LLM answers against a golden set:

- `exact` – byte-for-byte equality
- `normalized` – equality after case, punctuation, article and whitespace folding
- `token_f1` – SQuAD-style token overlap F1
- `numeric` – numbers compared with a relative tolerance, units ignored
- `json_fields` – expected fields must appear in a JSON answer with equal values

Why several matchers: "exact match" alone under-reports correct answers
("The Pacific Ocean." vs "pacific ocean"), while token F1 alone over-reports
partially right ones. Running them side by side on the same set shows how much
of a score is formatting noise.

Everything runs offline. Model calls sit behind a small provider interface and
the repo ships a fake provider that replays recorded answers.

## Usage

```
python3 -m answer_matchers data/golden.jsonl data/recorded_answers.jsonl
python3 -m unittest discover -s tests
```

Golden rows: `{"id", "expected", "matcher"}`. Answer rows: `{"id", "answer"}`.

## Layout

- `answer_matchers/normalize.py` – text folding
- `answer_matchers/matchers.py` – the matchers and a registry
- `answer_matchers/provider.py` – provider interface and fake replay provider
- `answer_matchers/report.py` – per-matcher accuracy table
- `data/` – fixture golden set and recorded answers

Numbers printed by the CLI come from the fixtures in `data/` and say so.

## Validation

`make validate` runs the unit tests and the fixture eval. On the 8-case fixture
set in `data/` the token F1 cases average 0.73 and the single exact-match case
scores 0.00 because the recorded answer differs only in case (`canberra`), which
the `normalized` matcher would accept. These are fixture results, not a benchmark.

## Caveats

- `numeric` reads the first number in the answer only.
- `json_fields` needs a bare JSON object; an answer wrapped in prose scores 0.
