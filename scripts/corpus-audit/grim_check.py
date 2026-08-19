"""GRIM-style check, tightly bound.

v1 paired any % with any nearby integer (50% hit rate, all noise).
v2 required an explicit "of" link but cross-paired ratios and percentages within
a sentence, so "14 of 15 (93%) ... 12 of 15 (80%)" produced four bogus flags.

v3 binds each figure to its own immediate neighbour only:
  A. "K of N (P%)"  -- percentage in the parenthetical directly after the ratio
  B. "P% of N"      -- denominator directly after the percentage
Nothing else counts.
"""
from __future__ import annotations
import re, sys, glob, json
from pathlib import Path

FENCE=re.compile(r"```.*?```",re.S); INLINE=re.compile(r"`[^`]+`"); HTML=re.compile(r"<[^>]+>")
# A: "12 of 34 CVEs (35%)" / "18 of them (36%)" — % must be in the parenthetical right after
A = re.compile(r"\b(\d{1,5})\s+of\s+(?:the\s+|them\s+|these\s+)?(\d{1,5})?\s*[\w\s-]{0,28}?\((\d{1,3}(?:\.\d{1,2})?)\s?%\)")
# B: "73% of 50 videos"
B = re.compile(r"(\d{1,3}(?:\.\d{1,2})?)\s?(?:%|percent)\s+of\s+(?:the\s+|my\s+|these\s+|those\s+|all\s+)?(\d{1,5})\b", re.I)

def clean(t): return HTML.sub(" ", INLINE.sub(" ", FENCE.sub(" ", t)))
def reachable(p,n,tol=0.5): return any(abs(100.0*k/n-p)<=tol for k in range(n+1))
def ok(n): return 3 <= n <= 5000 and not (1900 <= n <= 2100)

def analyse(path):
    t = clean(path.read_text(encoding="utf-8", errors="ignore"))
    out, pairs = [], 0
    for m in A.finditer(t):
        k, n, p = int(m.group(1)), m.group(2), float(m.group(3))
        if n is None: continue
        n = int(n)
        if k > n or not ok(n): continue
        pairs += 1
        actual = 100.0*k/n
        if abs(actual - p) > 1.0:
            out.append({"form":"A","file":path.name,"k":k,"n":n,"stated":p,
                        "actual":round(actual,2),"ctx":m.group(0)[:110]})
    for m in B.finditer(t):
        p, n = float(m.group(1)), int(m.group(2))
        if not (0 < p < 100) or not ok(n): continue
        pairs += 1
        if not reachable(p, n):
            out.append({"form":"B","file":path.name,"stated":p,"n":n,
                        "implies":round(p*n/100,2),"ctx":m.group(0)[:110]})
    return out, pairs

if __name__ == "__main__":
    allf, tot, nf = [], 0, 0
    for f in sorted(glob.glob(sys.argv[1])):
        r, pr = analyse(Path(f)); allf += r; tot += pr; nf += 1
    print(f"files={nf}  tightly-bound pairs={tot}  inconsistent={len(allf)}\n")
    Path("/tmp/grim/tight.json").write_text(json.dumps(allf, indent=1))
    for x in allf:
        if x["form"]=="A":
            print(f"  [A] {x['file'][:44]:46} {x['k']}/{x['n']} = {x['actual']}%  stated {x['stated']}%")
        else:
            print(f"  [B] {x['file'][:44]:46} {x['stated']}% of {x['n']} = {x['implies']} items")
        print(f"        …{x['ctx']}…")
