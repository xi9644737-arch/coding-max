import unittest

import worker


def retained_payload_count(payloads: list[bytes]) -> int:
    identities = {id(payload) for payload in payloads}
    retained = 0
    for value in vars(worker).values():
        if isinstance(value, dict):
            candidates = [*value.keys(), *value.values()]
        elif isinstance(value, (list, tuple, set, frozenset)):
            candidates = value
        else:
            continue
        retained += sum(id(candidate) in identities for candidate in candidates)
    return retained


class BoundedRetentionTests(unittest.TestCase):
    def setUp(self) -> None:
        reset = getattr(worker, "reset", None)
        if reset is not None:
            reset()

    def test_payloads_are_not_retained(self) -> None:
        payloads = [bytes([index]) * 30_000 for index in range(25)]
        for payload in payloads:
            self.assertEqual(worker.process(payload), len(payload))
        self.assertLessEqual(
            retained_payload_count(payloads),
            1,
            "worker module retains request payloads after processing",
        )


if __name__ == "__main__":
    unittest.main()
