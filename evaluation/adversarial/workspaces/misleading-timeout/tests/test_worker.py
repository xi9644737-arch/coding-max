import unittest

import worker


class WorkerTests(unittest.TestCase):
    def setUp(self) -> None:
        worker.reset()

    def test_sustained_requests_remain_available(self) -> None:
        for _ in range(40):
            self.assertEqual(worker.process(b"x" * 30_000), 30_000)


if __name__ == "__main__":
    unittest.main()
