"""Boundary/control checks for a small model; no hardware guarantees asserted."""

import unittest

from timelock_model import RetentionModel, experiment


class RetentionTests(unittest.TestCase):
    def test_long_frozen_lifetime_does_not_consume_retention(self):
        for unfreeze_at in (0, 1, 100, 10000):
            for mutation in ("write", "delete"):
                with self.subTest(unfreeze_at=unfreeze_at, mutation=mutation):
                    model = RetentionModel()
                    model.apply("advance_checker", unfreeze_at)
                    self.assertFalse(model.apply(mutation, "new"))
                    model.apply("unfreeze")
                    for tick in range(unfreeze_at, unfreeze_at + 8):
                        model.apply("advance_checker", tick)
                        self.assertFalse(model.apply(mutation, "new"))
                        self.assertEqual(model.value, "yesterday")
                    model.apply("advance_checker", unfreeze_at + 8)
                    self.assertTrue(model.apply(mutation, "new"))

    def test_identical_clock_attack_distinguishes_broken_control(self):
        results = []
        for broken in (False, True):
            model = RetentionModel(trust_host_clock=broken)
            model.apply("unfreeze")
            model.apply("set_host_clock", 1000)
            results.append(model.apply("delete"))
        self.assertEqual(results, [False, True])

    def test_clock_rollback_and_policy_edits_do_not_change_protection(self):
        model = RetentionModel()
        model.apply("advance_checker", 10)
        model.apply("unfreeze")
        for operation, argument in (("advance_checker", 0),
                                    ("shorten_retention", 0), ("unfreeze", None)):
            self.assertFalse(model.apply(operation, argument))
            self.assertEqual((model.now, model.expiry, model.value),
                             (10, 17, "yesterday"))

    def test_invalid_inputs_and_budget_fail_without_unbounded_work(self):
        for duration in (0, -1, True, "7"):
            with self.assertRaises(ValueError):
                RetentionModel(duration=duration)
        model = RetentionModel()
        for argument in (None, True, float("inf"), "1000"):
            self.assertFalse(model.apply("advance_checker", argument))
        model.operations = 1000
        with self.assertRaises(ValueError):
            model.apply("delete")
        self.assertEqual(model.value, "yesterday")

    def test_recorded_cases_include_expiry_and_failed_attack_controls(self):
        result = experiment()
        self.assertLessEqual(result["operations"], 1000)
        cases = {case["case"]: case for case in result["cases"]}
        self.assertIsNone(cases["unfreeze_starts_full_duration"]["events"][-1]["value"])
        self.assertEqual(cases["host_clock_forward_is_ignored"]["events"][-1]["value"],
                         "yesterday")
        self.assertIsNone(cases["broken_host_clock_positive_control"]["events"][-1]["value"])
        self.assertIsNone(cases["broken_creation_deadline_positive_control"]["events"][-1]["value"])
        self.assertEqual(cases["frozen_has_no_creation_deadline"]["events"][-1]["value"],
                         "yesterday")


if __name__ == "__main__":
    unittest.main()
