import unittest

from dedupe import deduplicate


class FunctionalTests(unittest.TestCase):
    def test_preserves_first_seen_order(self) -> None:
        self.assertEqual(deduplicate(["b", "a", "b", "c"]), ["b", "a", "c"])


if __name__ == "__main__":
    unittest.main()
