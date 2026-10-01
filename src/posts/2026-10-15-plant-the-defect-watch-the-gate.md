---
title: "Plant the Defect, Watch the Gate"
date: 2026-10-15
draft: false
author: William Zujkowski
description: "Mutation testing pointed at CI checks instead of code: plant a known defect, require the gate to go red, and put a floor under how much it examined. Seven mutations against this site's own required checks."
tags:
  - software-engineering
  - devops
  - testing
  - security
---

This site has four required checks. Branch protection will not merge a pull request until `remarque`, `axe`, `check-lint` and `pytest` report green on an up-to-date branch. One of the things `remarque` runs is a typography audit that enforces a 13px floor, and it announces which token it is guarding every time it starts:

```text
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  No violations found. (37 files scanned)
```

That output is from October 1, after I appended `:root { --text-micro: 0.5rem; }` to the site's stylesheet. Twelve declarations under `astro-site/src/` use `font-size: var(--text-micro)`. The audit names the token in its banner, then never reads it. Exit 0; the wrapper the `remarque` job calls also passed.

The audit is not broken in any way you can see from its output. That is the point of this post. A gate that cannot fail produces exactly the output of a gate that passed, so a green tick, by itself, carries no information about which one you have. The only way to find out is to hand the gate a defect you know is there and require it to go red. And because "red on a defect" says nothing about a run that examined nothing at all, the gate also needs a floor on how much it looked at.

<!-- DOODLE: a smoke detector on a ceiling with a person on a stepladder holding a lit match up to it; the detector's little light is green and calm while the smoke curls straight around it -->

## This is mutation testing, pointed at the referee

None of the method is new. Jia and Harman's [survey of mutation testing](https://doi.org/10.1109/TSE.2010.62) (IEEE TSE, 2011) describes faults "deliberately seeded into the original program, by simple syntactic changes," then run against the test set; a test set that cannot tell the mutant from the original has a hole. They trace the field to a 1971 student paper by Richard Lipton and to late-1970s papers including DeMillo, Lipton and Sayward's [*Hints on Test Data Selection*](https://doi.org/10.1109/C-M.1978.218136). Tools such as [Stryker](https://stryker-mutator.io/docs/) for JavaScript, C# and Scala, and [mutmut](https://mutmut.readthedocs.io/) for Python automate it. Stryker's vocabulary is the one worth borrowing: "If your tests *fail* then the mutant is *killed*. If your tests passed, the mutant *survived*."

Security people know the same move from a different shelf. The [EICAR test file](https://www.eicar.org/download-anti-malware-testfile/) exists so you can check that an anti-malware product actually responds without handing it real malware; EICAR's own comparison is that testing with live viruses "is rather like setting fire to the dustbin in your office to see whether the smoke detector is working."

The distinct part here is the target. Mutation testing is described in terms of the program under test: can the tests tell when the code is wrong? A CI gate is also a program that decides whether something is wrong, and it can be mutated the same way. There are two places to plant the mutation:

- **In the input.** Plant a defect in the content the gate inspects (an 8px font, a dead link) and require red. This tests the gate.
- **In the gate.** Break the scanner itself and see whether anything guarding the scanner notices. This tests the gate's tests.

The degenerate case needs no mutation at all. The original workflow in my [scanning-pipeline post](/posts/2025-10-06-automated-security-scanning-pipeline) had an aggregate security gate whose only step echoed a string. It could not fail, and nothing about its green tick said so.

## Seven mutations against the current main

Every row below ran on October 1 against commit `fc0c1eb` in a disposable worktree, with the tree restored and verified clean after each one. The commands and full output are in the [research note](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-10-01-plant-the-defect-watch-the-gate.md).

| Mutation | Gate that should notice | Result |
| --- | --- | --- |
| Control: a literal `font-size: 8px` | typography audit | **red**, exit 1 |
| `--text-micro` redefined as `0.5rem` | typography audit and the `remarque` wrapper | green, exit 0 |
| Audit's final `process.exit(1)` changed to `exit(0)` | `pnpm test:unit` | 56 of 56 pass |
| Audit's `scan()` counts each file, then returns | `pnpm test:unit` | 56 of 56 pass |
| Control: one of #652's regex fixes reverted | `pnpm test:unit` | **red**, 1 of 56 fails |
| Every test file in `scripts/ci/tests/` deleted | the required `pytest` command | 304 pass instead of 345, exit 0 |
| Posts moved one directory down | link monitor's three steps | 0 links from 0 files, all exit 0 |

The controls matter as much as the survivors. Without the first row, a reader could reasonably suspect the typography audit was simply dead; it is not, it catches the naive violation and nothing shaped differently. The stubbed scanner is the most unsettling row in practice: with an 8px declaration planted, it printed "No violations found. (37 files scanned)." It did count 37 files. It just stopped reading them. The exit-code mutation has its own flavour: the audit printed `[FAIL] styles/global.css:1645 → 8px`, then exited 0, which is a gate filing a complaint and approving the merge in the same breath.

The mirror image matters as much. A check that goes red on everything tells you as little as one that never does, which is why each planted defect needs a clean run beside it. Bo Chen's preprint [*From Runnable to Verifiable*](https://arxiv.org/abs/2608.09567) (arXiv, August 2026) audited artifacts from LLM- and agent-driven vulnerability research and ran their exploits against patched builds. In 20 of the 30 cases that reached a verdict, the claimed signal still appeared after the fix. Its conclusion carries straight over to a CI gate: a trigger on the vulnerable build is not evidence without a clean patched counterfactual.

## The tests I wrote to guard the gate

This is the second time the repo has been through this, and the first round is why the second one was needed.

In August, [#492](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/492) found that the then-only required check reported pass when the audit tool it wrapped never ran: no output meant zero failures meant exit 0. The follow-up sweep in [#511](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/511) planted 60-plus violations across 18 checkers. The accessibility suite passed 18 of 18 against an empty `dist/`, because a page that does not exist has no axe violations. [#516](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/516) fixed those with negative-control matrices.

In September, [#652](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/652) closed two more regex holes found the same way, and added tests. Those tests read the audit scripts as text and assert on the regex literals. They catch the control above: revert one of the fixes and they go red. They also passed every mutation that left the regexes alone and broke the enforcement around them. A later sweep, [#660](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/660), ran 79 mutations against three suites: 51 killed, 28 survived, four of the survivors equivalent. Its verdict on the #652 tests is the most accurate sentence in the thread: "It proves the patterns are right and proves nothing about whether the gate fires."

A test that checks the gate's spelling will pass while the gate does nothing. The fixture has to go through the same entry point CI uses and assert on the exit code. Anything shorter tests a model of the gate rather than the gate, which is the same gap the [formal-verification post](/posts/2026-07-30-prove-the-gate-not-the-agent) spent its second half closing with differential testing.

## A floor under what it looked at

Planting a defect shows the gate *can* fail. It says nothing about a run that examined nothing, and a run over nothing is clean in the most literal sense.

<div class="flow" role="group" aria-label="What a green required check has to establish before it means anything">
  <div class="flow-node"><b>Plant a known defect</b><i>one per rule the gate claims to enforce</i></div>
  <div class="flow-node is-gate"><b>Run the real entry point</b><i>the command CI runs, not a helper</i></div>
  <div class="flow-node is-gate"><b>Assert a floor</b><i>files, links or tests examined</i></div>
  <div class="flow-branch" role="group" aria-label="Outcomes">
    <div class="flow-leg" data-branch="Red" role="group" aria-label="Red"><div class="flow-node is-good"><b>Mutant killed</b><i>green now carries information</i></div></div>
    <div class="flow-leg" data-branch="Green" role="group" aria-label="Green"><div class="flow-node is-bad"><b>Mutant survived</b><i>the check is a label</i></div></div>
  </div>
</div>

The unit-test wrapper already has a floor, and its history shows how a floor goes soft. `MIN_TESTS` was 42 against 48 real tests. #652 recorded that seven of the ten test files could have been deleted with the floor still green, including the three files that exist as non-vacuity guards. It now sits at the exact count, 56: a ratchet, not a target.

The siblings have no floor. [#644](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/644) lists them: Playwright has no `forbidOnly`, so one stray `test.only` collapses the browser suite to a single green test, and pytest fails on zero collected tests only across *all* paths, which is how the deletion in the table lost 41 tests without complaint. The link pipeline ([#645](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/645)) uses a non-recursive glob. Against the flat directory, the extractor found 1,544 links in 97 files. Against the same 97 posts one level down, it found nothing, and the validator and summary agreed there was nothing wrong with nothing.

The most structural version is in #644 too. A required check that is *skipped* satisfies branch protection. Three September commits merged with all four required checks reporting `skipped`: correct for docs-only changes, and byte-for-byte what a crash in the job that decides "docs-only" would produce. I confirmed the check runs for all three through the GitHub API. The crash path has never been exercised: #644 found that the deciding job had not failed once in the last 30 runs of each workflow.

## What it costs, and where it stops

Google's [State of Mutation Testing at Google](https://doi.org/10.1145/3183519.3183521) (Petrović and Ivanković, ICSE-SEIP 2018) is mostly about cost: generating at most one mutant per covered line in a diff, suppressing "arid" lines such as logging, and treating developer attention as the scarce resource. With that feedback loop they report the usefulness of surfaced results improving from 20% to 80%. For a handful of CI gates the arithmetic is kinder: four required checks, each enforcing a short list of rules, so the mutants can be hand-written. That is my inference, not something the paper measured.

Two objections hold. First, equivalent mutants exist here too; #660 found that dropping an `is_link_local` check changed nothing because Python's `ipaddress` already treats those addresses as private. A survivor is a question, not a verdict. Second, a planted fixture only proves the gate catches that shape. The typography audit caught the literal 8px and missed the token. The useful source of mutations is what the gate claims about itself in its banner and its docstring. #660 found a compliance module whose docstring promises that scanning zero posts must exit non-zero, and no test checks it.

As of this writing, #642, #644, #645 and #660 are open, and the token mutation still passes on main. #642 already states the acceptance criterion: each fix ships with its planted mutation as a test that must go red. The sentence after it is the whole method, so it gets the last word: "A guard nobody has watched fail is a guard nobody knows works."
