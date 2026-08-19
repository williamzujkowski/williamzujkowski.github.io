---

author: William Zujkowski
date: 2026-08-18
description: "A gate that echoes a string and exits zero. A suppression field that does not exist. A scanner that reports clean because its error path returns an empty list. Notes from auditing every post I have written."
title: "Checks That Pass for the Wrong Reason"
tags:
  - security
  - devops
  - automation
---
I spent the last stretch auditing every post on this site against the code, configs and papers they describe. Ninety posts. The single most common defect was not a wrong number, though there were plenty of those. It was a **control that looked enforced and was not** — and in almost every case the thing that made it invisible was that it *passed*.

A failing check gets fixed on the afternoon it fails. A check that passes for the wrong reason can sit there for a year while you build on top of it.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/silent-gate.png'); width: min(250px, 66%); aspect-ratio: 400/421; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">hooked through, hanging open</p>

## The one that started it

The oldest instance is mine, and it is a naming problem before it is a technical one.

I built a convention for loading coding standards into a model's context. It looked like this:

```
@load [CS:python + TS:pytest + SEC:*]
```

I described it in writing as an "intelligent router." It is not a router. Nothing parses that line. It is a string in a file that a language model reads and usually honours, and "usually" is carrying the entire sentence.

I knew that when I wrote it. I still described it as a mechanism, because **the syntax I had chosen made it easy to believe.** It has brackets and a namespace and a wildcard. It looks like an API call, so I reasoned about it like an API call, and for months I thought I had built enforcement when I had built a strong suggestion.

That is the general shape. The name and the shape of a thing quietly set your expectations for it, and then you stop checking whether those expectations hold.

## Six ways a check passes without checking

Auditing the rest of the archive, the same defect kept arriving in different costumes.

### 1. The gate that cannot fail

A CI pipeline I wrote up had a job named `security-gate`. Its whole body:

```yaml
security-gate:
  needs: [dependency-scan, container-scan, comprehensive-scan]
  if: always()
  steps:
    - name: Evaluate security posture
      run: |
        echo "All security scans completed"
        # Download and analyze all SARIF reports
        # Make final go/no-go decision
```

The go/no-go decision is a comment. `if: always()` is there for a good reason — you want the gate to report even when an upstream job failed rather than being skipped — but it also means the gate **passes when everything upstream fails**, unless it explicitly reads `needs.<job>.result`. Which it did not.

Same family, different tool: a colour-space project had a build gate asserting that every value round-trips within ΔE 1.0. It re-derived everything from the source hex in floating point and never read the rounded values actually written to disk. So it could only ever measure IEEE-754 noise. Corpus maximum: **5.67e-13**, against a threshold of 1.0. Twelve orders of magnitude of headroom, and structurally incapable of failing. The specific scenario it existed to catch — a rounding change in a dependency — happens in the step it was not looking at.

Both of these are green checkmarks. Both have been green the whole time.

### 2. The key that does not exist

A grype config had this, presented as time-boxed risk acceptance:

```yaml
ignore:
  - vulnerability: CVE-2023-12345
    reason: "Not applicable - feature not used"
    expiration: 2025-12-31
```

Grype's `IgnoreRule` struct has these fields: `Vulnerability`, `IncludeAliases`, `Reason`, `Namespace`, `FixState`, `Package`, `VexStatus`, `VexJustification`, `MatchType`.

There is no `expiration`. YAML parsers do not object to keys nobody reads. So the suppression is permanent, and by the time I found it the date had been in the past for eight months while the finding stayed hidden.

Worse in the same repository: an entire `osv-scanner.toml` of invented keys — `[scanning]`, `workers`, `max_depth`, `skip_git` — none of which appear in the tool's schema. And a benchmark attached to one of them: *"set `workers = 4` for parallel scanning (40% faster on my 8-core system)."* That is a measurement of a configuration key that has never existed. It cannot have been taken. It reads like it was.

**This is the most dangerous variant**, because the reader can verify it and still be wrong. The field names are plausible. Some of them are real flags from adjacent tools. Checking that a key looks right is not checking that the tool reads it.

### 3. The flag whose semantics are backwards

A Trivy policy, described as denying builds on critical findings:

```bash
trivy image --policy ./policy/security.rego myapp:latest
```

Two problems. The flag is `--ignore-policy`; there is no `--policy` for this, so the command errors on an unknown flag. And the name is the semantics: a Trivy Rego policy **filters findings out**. It cannot deny, block, or fail anything.

So a policy written to "deny on critical" is, under the only mechanism the tool offers, either inert or a rule that *suppresses* criticals. The second outcome is the one that should worry you, and it is the one that happens if someone helpfully fixes the flag.

The kernel has a well-known instance of the same trap. `CONFIG_KEXEC_SIG` sounds like it makes `kexec_file_load` require a signed kernel. The Kconfig help text says otherwise, in as many words: *"The image can still be loaded without a valid signature unless you also enable KEXEC_SIG_FORCE."* A post I wrote claimed the former. The refusal actually comes from lockdown, which needs Secure Boot enforcing — so on a machine with Secure Boot off, the option named for signature verification verifies nothing.

### 4. The error swallowed into a pass

This is the one with the highest blast radius, because it converts an outage into an all-clear.

A vulnerability scanner queried the NVD API like this:

```python
params = {"keyword": package_name, ...}
```

The NVD 2.0 parameter is `keywordSearch`. I tested both against the live API: `keyword` returns **404**, `keywordSearch` returns 200. Then follow the error path — `raise_for_status()` raises, `except requests.RequestException` catches, and the handler does `return []`. That empty list propagates all the way up to the report, which prints:

```
Total vulnerabilities: 0
```

Every host, every run, clean. And the same file had a second, independent instance: version comparison caught `packaging.version.InvalidVersion` and returned `False`, meaning *not vulnerable*. Every real Debian and Ubuntu version string raises it — `1:24.0.5-1`, `9.2p1-2ubuntu0.13`, `3.0.2-0ubuntu1.12` — so every package it looked at cleared.

Two bugs, written months apart, both failing in the same direction. That is not coincidence; it is what happens when the quiet path is never exercised.

A threat-intelligence lookup in another post did the same thing three ways at once. It called `os.environ` without importing `os`, so it raised `NameError` on its first line and had never run at all. Behind that, the field name was wrong and nested one level too shallow, so `.get(..., 0)` would have returned 0 for a confirmed-malicious address. And `return 0` on any non-200 meant the free tier's daily rate limit turned every attacker benign after the first HTTP 429.

**If a check cannot answer, it must not answer "fine."** A scanner that returns "no findings" on a network error is worse than no scanner, because you stop looking.

### 5. The check that cannot run when it matters

A pre-commit hook enforcing standards, and the honest discovery that you can walk straight past it:

```bash
git commit --no-verify
```

My instinct at the time was to close the hole from inside the hook. You cannot. `--no-verify` skips the hook entirely — the process never starts, so nothing it might do on the way out can matter. There is no exit code that runs when the code does not run.

Client-side hooks are a convenience for the person running them. Enforcement is server-side: a `pre-receive` hook, a required status check, branch protection. Keep the hook for the fast feedback loop; do not confuse it for the control.

Adjacent: a Prometheus config whose `rule_files` glob matched nothing, because the rules directory was never mounted into the container. That is not a startup error. Prometheus comes up healthy with **zero rules loaded**, which looks exactly like a quiet night.

### 6. The test that asserts the defect

The one I find most uncomfortable, because tests are supposed to be the answer to all of the above.

A link validator was classifying transient server errors as dead links. Its regression test:

```python
@pytest.mark.parametrize("code,expected", [
    (404, "broken"),
    (500, "broken"),
    (503, "broken"),
])
```

That test passes. It has always passed. It was written from the implementation rather than from the intent, so it faithfully locks in the behaviour the implementation happens to have — including the wrong parts. A 5xx means the origin answered and erred. It is up. Treating that as a dead citation fed live sources into an auto-repair queue that rewrites links.

The fix was to state the taxonomy as an invariant instead of a table of examples:

```python
def test_only_dead_codes_are_broken():
    broken = {c for c in range(200, 600) if classify(c)[0] == "broken"}
    assert broken == {404, 410}
```

That version cannot be satisfied by the bug.

## The near-miss, which is the actual point

I would like to claim I am now immune to this. Last night says otherwise.

I was testing whether a static site could drop `'unsafe-inline'` from its Content-Security-Policy by having the framework hash every inline script at build time. I enabled it, rebuilt, and checked the output:

```
inline scripts on the page: 8
sha256 hashes in the policy: 8
'unsafe-inline' present:     no
```

Eight and eight. No unsafe-inline. I nearly shipped it.

The count match was a coincidence. Computing the actual SHA-256 of each script body and testing membership in the policy:

```
[0] type="application/ld+json"   NO MATCH
[1] type="application/ld+json"   NO MATCH
[2] (theme-flash)                NO MATCH
[4]                              MATCH
[5]                              MATCH
[6] (theme deck)                 NO MATCH
[7] (theme toggle)               NO MATCH
[8] (mobile TOC)                 NO MATCH
```

Two of eight. Across a 25-page sample, **133 of 183 inline scripts would have been blocked.** The framework only hashes scripts it compiles, and every one of those had an `is:inline` directive — which is a direct instruction not to process them.

And the failure would have been silent, because `report-uri` is also ignored when CSP arrives in a `<meta>` tag. No telemetry. The symptom would have been readers getting a flash of the wrong theme and a dead theme picker, with every check green.

I caught it because I had spent a week reading other people's broken gates and had gotten suspicious of tidy numbers. **The count was the check that passed for the wrong reason.**

## What to actually do

Nothing here is clever. It is all just declining to accept the cheap signal.

**Verify the mechanism, not the presence of the mechanism.** The question is never "is there a gate." It is "what happens when I feed it something that should fail." Break it on purpose once, and watch it break.

**Grep the tool's source or schema for the key you are about to rely on.** Every invented config key in this archive would have died to a thirty-second search of the struct definition. A key that looks right and a key the parser reads are different things, and only one of them is checkable.

**Make errors loud, and never let them return the safe value.** `return []`, `return 0`, `return False` on an exception path are all the same bug with different types. If the check cannot evaluate, it must raise, and something must alert on the absence of a result rather than only on a bad one.

**Write tests from the intent, and prefer invariants to examples.** "The broken set is exactly `{404, 410}`" cannot be satisfied by a bug. A list of cases can be, and will be, because the list gets written by reading the code.

**Be suspicious when a number comes out clean.** Eight and eight. A false-positive rate of exactly zero. Twelve orders of magnitude of headroom. A tidy result is a hypothesis, not a conclusion, and the cheapest moment to check it is while you still believe it.

The uncomfortable summary of ninety posts: almost every control I had written up as working had a plausible story, a passing check, and a green light. The ones that were actually broken were not the ones that looked broken. They were the ones nobody had tried to break.
