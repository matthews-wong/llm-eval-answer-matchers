import unittest

from answer_matchers.matchers import score


class MatcherTest(unittest.TestCase):
    def test_exact_is_strict(self):
        self.assertEqual(score("exact", "Paris", "paris"), 0.0)
        self.assertEqual(score("exact", "Paris", "Paris"), 1.0)

    def test_normalized_ignores_formatting(self):
        self.assertEqual(score("normalized", "Pacific Ocean", "The Pacific Ocean."), 1.0)

    def test_token_f1_partial_credit(self):
        self.assertAlmostEqual(score("token_f1", "new york city", "new york"), 0.8)

    def test_token_f1_disjoint_and_empty(self):
        self.assertEqual(score("token_f1", "cat", "dog"), 0.0)
        self.assertEqual(score("token_f1", "", ""), 1.0)
        self.assertEqual(score("token_f1", "cat", ""), 0.0)

    def test_numeric_tolerance_and_separators(self):
        self.assertEqual(score("numeric", "1000", "about 1,005 units"), 1.0)
        self.assertEqual(score("numeric", "1000", "1,100"), 0.0)

    def test_numeric_no_number_in_answer(self):
        self.assertEqual(score("numeric", "42", "many"), 0.0)

    def test_numeric_bad_expected_is_an_error(self):
        with self.assertRaisesRegex(ValueError, "no number"):
            score("numeric", "n/a", "3")

    def test_json_fields_subset_match(self):
        self.assertEqual(score("json_fields", '{"a": 1}', '{"a": 1, "b": 2}'), 1.0)
        self.assertEqual(score("json_fields", '{"a": 1}', '{"a": 2}'), 0.0)

    def test_json_fields_rejects_malformed_answer(self):
        self.assertEqual(score("json_fields", '{"a": 1}', "not json"), 0.0)
        self.assertEqual(score("json_fields", '{"a": 1}', "[1]"), 0.0)

    def test_unknown_matcher_names_the_choices(self):
        with self.assertRaisesRegex(KeyError, "unknown matcher 'fuzzy'"):
            score("fuzzy", "a", "a")


if __name__ == "__main__":
    unittest.main()
