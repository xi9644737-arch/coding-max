import unittest

from dedupe import deduplicate


class CountedString(str):
    comparisons = 0
    __hash__ = str.__hash__

    def __eq__(self, other: object) -> bool:
        type(self).comparisons += 1
        return super().__eq__(other)


class PerformanceTests(unittest.TestCase):
    def test_unique_batch_comparison_budget(self) -> None:
        values = [CountedString(f"item-{index}") for index in range(2_000)]
        CountedString.comparisons = 0
        self.assertEqual(deduplicate(values), values)
        self.assertLess(
            CountedString.comparisons,
            10_000,
            f"batch used {CountedString.comparisons} equality comparisons",
        )


if __name__ == "__main__":
    unittest.main()
