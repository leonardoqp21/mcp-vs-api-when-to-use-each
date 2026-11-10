import json
import pathlib
import unittest

from decide import QUESTIONS, decide

CASES = json.loads((pathlib.Path(__file__).parent / "cases.json").read_text())


class DecideTests(unittest.TestCase):
    def test_every_case(self):
        for case in CASES:
            with self.subTest(task=case["task"]):
                self.assertEqual([p["option"] for p in decide(case["answers"])], case["expected"])

    def test_every_pick_has_a_reason(self):
        for case in CASES:
            for pick in decide(case["answers"]):
                self.assertTrue(pick["why"].strip())

    def test_missing_answers_are_an_error(self):
        with self.assertRaises(ValueError):
            decide({"event_driven": True})

    def test_every_question_is_exercised(self):
        for key in QUESTIONS:
            self.assertTrue(any(c["answers"][key] for c in CASES), key)


if __name__ == "__main__":
    unittest.main()
