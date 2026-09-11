#!/usr/bin/env python3
"""Offline retention state model, not Timelock Drive code or a security boundary.

Only synthetic strings and integer ticks are used. No device, network, process,
credential, or backup access. Run prints a bounded experiment as JSON to stdout.
"""

import json
from dataclasses import dataclass


@dataclass
class RetentionModel:
    """Trusted-state assumption made explicit; Python callers can bypass it.

    Frozen blocks stay protected until unfreeze starts their original duration.
    Expiry is conservative: mutation requires time strictly greater than expiry.
    `trust_host_clock` is a deliberately broken comparison, not a supported mode.
    """

    duration: int = 7
    now: int = 0
    host_now: int = 0
    expiry: int | None = None
    value: str | None = "yesterday"
    trust_host_clock: bool = False
    operations: int = 0

    def __post_init__(self):
        if type(self.duration) is not int or self.duration <= 0:
            raise ValueError("duration must be a positive integer")

    def apply(self, operation: str, argument=None) -> bool:
        if self.operations >= 1000:
            raise ValueError("synthetic operation budget exhausted")
        self.operations += 1
        if operation == "advance_checker":
            if type(argument) is not int or argument < self.now:
                return False
            self.now = argument
            return True
        if operation == "set_host_clock":
            if type(argument) is not int:
                return False
            self.host_now = argument
            return True
        if operation == "unfreeze":
            if self.expiry is not None:
                return False
            self.expiry = self.now + self.duration
            return True
        if operation == "shorten_retention":
            return False
        if operation not in {"write", "delete"}:
            return False
        effective_now = self.host_now if self.trust_host_clock else self.now
        if self.expiry is None or effective_now <= self.expiry:
            return False
        if operation == "write" and not isinstance(argument, str):
            return False
        self.value = argument if operation == "write" else None
        return True


def run_case(name, actions, *, broken=False, creation_deadline=False):
    model = RetentionModel(trust_host_clock=broken)
    if creation_deadline:
        model.expiry = model.now + model.duration
    events = []
    for operation, argument in actions:
        accepted = model.apply(operation, argument)
        events.append({
            "operation": operation, "argument": argument, "accepted": accepted,
            "checker_tick": model.now, "host_tick": model.host_now,
            "expiry_tick": model.expiry, "value": model.value,
        })
    return {"case": name, "broken_clock_control": broken,
            "broken_creation_deadline_control": creation_deadline,
            "operations": model.operations, "events": events}


def experiment():
    attack = [("unfreeze", None), ("set_host_clock", 1000), ("delete", None)]
    cases = [
        run_case("frozen_has_no_creation_deadline", [
            ("advance_checker", 100), ("write", "replacement"), ("delete", None),
        ]),
        run_case("broken_creation_deadline_positive_control", [
            ("advance_checker", 100), ("delete", None),
        ], creation_deadline=True),
        run_case("unfreeze_starts_full_duration", [
            ("advance_checker", 100), ("unfreeze", None),
            ("advance_checker", 106), ("delete", None),
            ("advance_checker", 107), ("delete", None),
            ("advance_checker", 108), ("delete", None),
        ]),
        run_case("early_overwrite_and_shortening", [
            ("unfreeze", None), ("shorten_retention", 0),
            ("write", "replacement"), ("unfreeze", None), ("delete", None),
        ]),
        run_case("host_clock_forward_is_ignored", attack),
        run_case("broken_host_clock_positive_control", attack, broken=True),
        run_case("checker_rollback_is_rejected", [
            ("unfreeze", None), ("advance_checker", 6),
            ("advance_checker", 0), ("delete", None),
            ("advance_checker", 8), ("write", "replacement"),
        ]),
        run_case("host_clock_rollback_does_not_extend_expiry", [
            ("unfreeze", None), ("set_host_clock", -1000),
            ("advance_checker", 8), ("delete", None),
        ]),
    ]
    total = sum(case["operations"] for case in cases)
    assert total <= 1000
    return {
        "schema_version": 1, "kind": "original offline state-model exercise",
        "not_a_timelock_drive_replication": True,
        "time_unit": "synthetic integer tick", "duration_ticks": 7,
        "expiry_rule": "checker_tick > unfreeze_tick + duration_ticks",
        "operation_budget": 1000, "operations": total, "cases": cases,
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
