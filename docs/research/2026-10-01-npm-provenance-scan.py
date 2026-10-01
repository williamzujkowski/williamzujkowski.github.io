"""Find jagreehal-maintained versions published 2026-06-03..06-05 that still exist,
and fetch their npm attestations. Read-only public registry reads."""
import json, urllib.request, urllib.parse, time, pathlib, base64

RAW = pathlib.Path(__file__).parent / "raw"
names = [o["package"]["name"] for o in json.loads((RAW / "search_jag.json").read_text())["objects"]]

def get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""

out = []
for n in names:
    st, body = get("https://registry.npmjs.org/" + urllib.parse.quote(n, safe="@"))
    if st != 200:
        continue
    pk = json.loads(body)
    vers = pk.get("versions", {})
    for v, t in pk.get("time", {}).items():
        if v in ("created", "modified") or not ("2026-06-03" <= t <= "2026-06-06"):
            continue
        rec = {"pkg": n, "ver": v, "time": t, "present": v in vers}
        if v in vers:
            s, b = get(f"https://registry.npmjs.org/-/npm/v1/attestations/{n}@{v}")
            rec["att_status"] = s
            if s == 200:
                (RAW / f"jag_att_{n.replace('/', '_')}_{v}.json").write_bytes(b)
                for a in json.loads(b)["attestations"]:
                    if a["predicateType"] == "https://slsa.dev/provenance/v1":
                        p = json.loads(base64.b64decode(a["bundle"]["dsseEnvelope"]["payload"]))
                        bd = p["predicate"]["buildDefinition"]
                        rec["ref"] = bd["externalParameters"]["workflow"]["ref"]
                        rec["path"] = bd["externalParameters"]["workflow"]["path"]
                        rec["repo"] = bd["externalParameters"]["workflow"]["repository"]
                        rec["event"] = bd["internalParameters"]["github"]["event_name"]
                        rec["commit"] = bd["resolvedDependencies"][0]["digest"]["gitCommit"]
                        rec["run"] = p["predicate"]["runDetails"]["metadata"]["invocationId"]
        out.append(rec)
    time.sleep(0.2)

(RAW / "jag_scan.json").write_text(json.dumps(out, indent=1))
print(len(out), "versions in window;", sum(r["present"] for r in out), "present")
for r in sorted(out, key=lambda r: r["time"]):
    print(r["time"], r["pkg"], r["ver"], r["present"], r.get("att_status"), r.get("event"), r.get("ref"), r.get("path"))
