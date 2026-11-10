.PHONY: validate test eval

validate: test eval ## Run every local check

test:
	python3 -m unittest discover -s tests

eval:
	python3 -m answer_matchers data/golden.jsonl data/recorded_answers.jsonl
