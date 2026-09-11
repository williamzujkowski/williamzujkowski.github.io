"""Offline method checks; timing itself has no environment-independent threshold."""

import unittest
from collections import Counter

from page_cache import CONDITIONS, schedule, summarize


class MethodTests(unittest.TestCase):
    def test_balanced_randomized_schedule_is_reproducible_and_bounded(self):
        rows = schedule(12, 33, 100)
        self.assertEqual(rows, schedule(12, 33, 100))
        self.assertNotEqual(rows, schedule(12, 34, 100))
        self.assertEqual(Counter(condition for condition, _ in rows),
                         dict.fromkeys(CONDITIONS, 12))
        self.assertTrue(all(0 <= page < 100 for _, page in rows))
        for count in (0, 101):
            with self.assertRaises(ValueError):
                schedule(count, 1, 100)

    def test_failed_eviction_and_outlier_remain_in_denominator(self):
        rows = [{"condition": "shared_file", "resident_before_prime": before,
                 "resident_after_prime": True, "resident_after_probe": True,
                 "probe": {"read_ns": latency}}
                for before, latency in ((False, 100), (True, 10000), (False, 200))]
        result = summarize(rows)["shared_file"]
        self.assertEqual(result["trials"], 3)
        self.assertEqual(result["resident_before_prime"], 1)
        self.assertEqual(result["median_read_ns"], 200)
        self.assertEqual(result["max_read_ns"], 10000)


if __name__ == "__main__":
    unittest.main()
