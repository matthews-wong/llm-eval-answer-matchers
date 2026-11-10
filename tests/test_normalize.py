import unittest

from answer_matchers.normalize import normalize, tokens


class NormalizeTest(unittest.TestCase):
    def test_folds_case_punctuation_and_articles(self):
        self.assertEqual(normalize("The Pacific Ocean."), "pacific ocean")

    def test_collapses_whitespace(self):
        self.assertEqual(normalize("  a   b\n c "), "b c")

    def test_unicode_compatibility_forms(self):
        self.assertEqual(normalize("ＡＢＣ"), "abc")

    def test_tokens_of_empty_string(self):
        self.assertEqual(tokens(""), [])


if __name__ == "__main__":
    unittest.main()
