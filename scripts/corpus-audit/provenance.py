"""Which model created each post, and what objective defect markers did it carry
BEFORE the audit corrected them."""
import subprocess, re, json, glob
from pathlib import Path
from datetime import date

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, cwd="/home/william/git/williamzujkowski.github.io").stdout

def model_of(body: str) -> str:
    m = re.search(r"Co-[Aa]uthored-[Bb]y:\s*(Claude[^<\n]*)", body)
    if m:
        s = m.group(1).strip()
        s = re.sub(r"\s*\(1M context\)", "", s).strip()
        return s if s != "Claude" else "Claude (unversioned)"
    for pat, name in [(r"codex", "codex"), (r"gemini", "gemini")]:
        if re.search(pat, body, re.I): return name
    return "unlabelled"

rows = []
for p in sorted(glob.glob("/tmp/grim/pre/src/posts/*.md")):
    name = Path(p).name
    # creating commit for this path
    log = sh("git", "log", "--diff-filter=A", "--format=%H|%ad", "--date=short",
             "--follow", "--", f"src/posts/{name}")
    if not log.strip(): continue
    sha, cdate = log.strip().split("\n")[-1].split("|")
    body = sh("git", "log", "-1", "--format=%s%n%b", sha)
    text = Path(p).read_text(errors="ignore")

    # frontmatter date
    fm = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    pdate = fm.group(1) if fm else cdate

    body_only = re.sub(r"```.*?```", " ", text, flags=re.S)
    nums = len(re.findall(r"(?<![\w.])\d{1,3}(?:\.\d+)?%|(?<![\w.$])\b\d{2,}\b", body_only))
    cites = len(re.findall(r"https?://", body_only))
    placeholders = len(re.findall(r"X{4,}|xxxx|CVE-\d{4}-X", text))
    # citations dated after the post
    future = 0
    for m in re.finditer(r"/(20\d{2})/(\d{2})/(\d{2})/|arxiv\.org/abs/(\d{2})(\d{2})\.", text):
        try:
            if m.group(1):
                if date(int(m.group(1)), int(m.group(2)), int(m.group(3))) > date.fromisoformat(pdate): future += 1
            elif m.group(4):
                yy, mm = 2000+int(m.group(4)), int(m.group(5))
                if date(yy, mm, 1) > date.fromisoformat(pdate): future += 1
        except Exception: pass

    rows.append({"post": name, "created": cdate, "post_date": pdate,
                 "model": model_of(body), "nums": nums, "cites": cites,
                 "ratio": round(nums/max(cites,1), 1),
                 "placeholders": placeholders, "future_cites": future})

Path("/tmp/grim/prov.json").write_text(json.dumps(rows, indent=1))
from collections import Counter
print("posts:", len(rows))
print("\nby creating model:")
for m, c in Counter(r["model"] for r in rows).most_common():
    print(f"  {m:28} {c}")
