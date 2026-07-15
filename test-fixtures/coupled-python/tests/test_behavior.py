import unittest

from app import api, cli
from app.state import FEATURE_FLAGS


class FeatureContractTests(unittest.TestCase):
    def setUp(self) -> None:
        FEATURE_FLAGS.clear()

    def test_cli_normalizes_feature_name(self) -> None:
        self.assertEqual(cli.enable_feature("  SEARCH  "), "search")
        self.assertTrue(FEATURE_FLAGS["search"])

    def test_api_uses_the_same_normalization_contract(self) -> None:
        self.assertEqual(api.enable_feature({"name": "  SEARCH  "}), "search")
        self.assertTrue(FEATURE_FLAGS["search"])


if __name__ == "__main__":
    unittest.main()
