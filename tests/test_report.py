import tempfile
import unittest
from pathlib import Path

from answer_matchers.__main__ import main
from answer_matchers.provider import ReplayProvider
from answer_matchers.report import evaluate, format_report, load_golden

DATA = Path(__file__).resolve().parent.parent / "data"


class ReportTest(unittest.TestCase):
    def test_fixture_scores_are_stable(self):
        golden = load_golden(DATA / "golden.jsonl")
        provider = ReplayProvider.from_jsonl(DATA / "recorded_answers.jsonl")
        scores = {case_id: value for case_id, _, value in evaluate(golden, provider)}
        self.assertEqual(len(scores), 8)
        self.assertEqual(scores["capital"], 0.0)
        self.assertEqual(scores["ocean"], 1.0)
        self.assertAlmostEqual(scores["bridge"], 2 / 3)

    def test_report_states_dataset_size(self):
        text = format_report([("a", "exact", 1.0)], "tiny.jsonl")
        self.assertIn("1 cases from tiny.jsonl", text)

    def test_missing_recorded_answer_names_the_case(self):
        with self.assertRaisesRegex(KeyError, "'ghost'"):
            ReplayProvider({}).complete("ghost")

    def test_golden_row_missing_key_names_file_and_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text('{"id": "x"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"bad.jsonl:1: missing \['expected', 'matcher'\]"):
                load_golden(path)

    def test_cli_usage_error(self):
        self.assertEqual(main([]), 2)


if __name__ == "__main__":
    unittest.main()
