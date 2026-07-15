import unittest

from names import normalize_name


class NameContractTests(unittest.TestCase):
    def test_hyphen_is_preserved(self) -> None:
        self.assertEqual(normalize_name("  Mary-Jane  "), "Mary-Jane")


if __name__ == "__main__":
    unittest.main()
