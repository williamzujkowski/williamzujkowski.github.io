#!/usr/bin/env python3
"""Bounded own-file, cross-process page-cache observation; not a VM attack."""

import argparse
import ctypes
import hashlib
import json
import mmap
import os
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import tempfile
import time

CONDITIONS = ("shared_file", "independent_file", "no_prime")
FILE_BYTES = 8 * 1024 * 1024


def schedule(repetitions, seed, pages):
    if not 1 <= repetitions <= 100 or pages < 1:
        raise ValueError("repetitions must be 1..100; pages must be positive")
    rng = random.Random(seed)
    rows = [(condition, rng.randrange(pages))
            for condition in CONDITIONS for _ in range(repetitions)]
    rng.shuffle(rows)
    return rows


def resident(fd, offset, page_size):
    """Snapshot one own-file page without intentionally reading its contents."""
    libc = ctypes.CDLL(None, use_errno=True)
    libc.mincore.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                            ctypes.POINTER(ctypes.c_ubyte))
    libc.mincore.restype = ctypes.c_int
    with mmap.mmap(fd, page_size, access=mmap.ACCESS_COPY, offset=offset) as mapping:
        address = ctypes.addressof(ctypes.c_char.from_buffer(mapping))
        state = ctypes.c_ubyte()
        if libc.mincore(address, page_size, ctypes.byref(state)) != 0:
            raise OSError(ctypes.get_errno(), "mincore failed")
        return bool(state.value & 1)


def worker(fd, offset, size):
    started = time.perf_counter_ns()
    data = os.pread(fd, size, offset)
    elapsed = time.perf_counter_ns() - started
    if len(data) != size:
        raise ValueError("short read")
    return {"read_ns": elapsed, "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data)}


def child_read(fd, offset, size):
    completed = subprocess.run(
        [sys.executable, "-I", str(Path(__file__).resolve()), "worker",
         str(fd), str(offset), str(size)],
        pass_fds=(fd,), check=True, capture_output=True, text=True, timeout=5,
    )
    return json.loads(completed.stdout)


def summarize(trials):
    results = {}
    for condition in CONDITIONS:
        rows = [row for row in trials if row["condition"] == condition]
        if rows:
            times = [row["probe"]["read_ns"] for row in rows]
            results[condition] = {
                "trials": len(rows),
                "resident_before_prime": sum(row["resident_before_prime"] for row in rows),
                "resident_after_prime": sum(row["resident_after_prime"] for row in rows),
                "resident_after_probe": sum(row["resident_after_probe"] for row in rows),
                "median_read_ns": statistics.median(times),
                "min_read_ns": min(times), "max_read_ns": max(times),
            }
    return results


def run(output, repetitions=60, seed=20260911, scratch_parent=None):
    if sys.platform != "linux" or not hasattr(os, "posix_fadvise"):
        raise RuntimeError("requires Linux, mincore, and posix_fadvise")
    page_size = mmap.PAGESIZE
    plan = schedule(repetitions, seed, FILE_BYTES // page_size)
    trials = []
    report = {
        "schema": 1, "scope": "synthetic own-file cross-process mechanism demonstration",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": platform.python_version(), "kernel": platform.release(),
        "machine": platform.machine(), "euid": os.geteuid(),
        "page_bytes": page_size, "file_bytes": FILE_BYTES,
        "seed": seed, "repetitions_per_condition": repetitions,
        "scratch_parent": str(Path(scratch_parent or tempfile.gettempdir()).resolve()),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "trials": trials, "status": "started",
    }
    # Refuse to overwrite prior evidence. Temporary files are generated here only.
    with Path(output).open("x") as evidence:
        try:
            with tempfile.TemporaryDirectory(prefix="page-cache-lab-", dir=scratch_parent) as directory:
                data = random.Random(seed).randbytes(FILE_BYTES)
                report["fixture_sha256"] = hashlib.sha256(data).hexdigest()
                paths = [Path(directory) / name for name in ("target.bin", "independent.bin")]
                for path in paths:
                    with path.open("xb") as fixture:
                        fixture.write(data)
                        fixture.flush()
                        os.fsync(fixture.fileno())
                del data
                with paths[0].open("rb") as target, paths[1].open("rb") as independent:
                    descriptors = (target.fileno(), independent.fileno())
                    report["distinct_inodes"] = os.fstat(descriptors[0]).st_ino != os.fstat(descriptors[1]).st_ino
                    if not report["distinct_inodes"]:
                        raise RuntimeError("independent fixture unexpectedly shares inode")
                    deadline = time.monotonic() + 300
                    for index, (condition, page) in enumerate(plan):
                        if time.monotonic() > deadline:
                            raise TimeoutError("five-minute experiment budget exceeded")
                        offset = page * page_size
                        for fd in descriptors:
                            os.posix_fadvise(fd, 0, FILE_BYTES, os.POSIX_FADV_DONTNEED)
                        before = resident(descriptors[0], offset, page_size)
                        prime = None
                        if condition != "no_prime":
                            prime_fd = descriptors[0 if condition == "shared_file" else 1]
                            prime = child_read(prime_fd, offset, page_size)
                        after = resident(descriptors[0], offset, page_size)
                        probe = child_read(descriptors[0], offset, page_size)
                        row = {"index": index, "condition": condition, "offset": offset,
                               "resident_before_prime": before, "resident_after_prime": after,
                               "resident_after_probe": resident(descriptors[0], offset, page_size),
                               "prime": prime, "probe": probe}
                        trials.append(row)
                        if prime and prime["sha256"] != probe["sha256"]:
                            raise RuntimeError("fixture content mismatch")
                    report["status"] = "complete"
        except Exception as error:
            report["status"] = "error"
            report["error"] = f"{type(error).__name__}: {error}"
            raise
        finally:
            report["summary"] = summarize(trials)
            report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            json.dump(report, evidence, indent=2)
            evidence.write("\n")
    print(json.dumps(report["summary"], indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    experiment = subparsers.add_parser("run")
    experiment.add_argument("--output", required=True)
    experiment.add_argument("--repetitions", type=int, default=60)
    experiment.add_argument("--seed", type=int, default=20260911)
    experiment.add_argument("--scratch-parent", help="existing directory for generated disposable files")
    reader = subparsers.add_parser("worker")
    for name in ("fd", "offset", "size"):
        reader.add_argument(name, type=int)
    args = parser.parse_args()
    if args.command == "worker":
        if args.fd < 0 or args.offset < 0 or args.size != mmap.PAGESIZE:
            parser.error("worker accepts a passed descriptor and exactly one page")
        print(json.dumps(worker(args.fd, args.offset, args.size)))
    else:
        run(args.output, args.repetitions, args.seed, args.scratch_parent)


if __name__ == "__main__":
    main()
