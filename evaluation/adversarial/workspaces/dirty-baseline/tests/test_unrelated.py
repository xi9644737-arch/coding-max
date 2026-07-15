import unittest


class UnrelatedBaselineTests(unittest.TestCase):
    def test_legacy_report(self) -> None:
        self.assertEqual("legacy", "modern")


if __name__ == "__main__":
    unittest.main()
