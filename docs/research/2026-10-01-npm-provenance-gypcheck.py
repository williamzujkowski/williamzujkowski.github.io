"""Check still-present jagreehal burst versions from jag_scan.json.

Default (metadata only, no package content downloaded):
  - the packument's dist.integrity (sha512) equals the attestation subject digest
  - the version carries an npm deprecation notice

--fetch-malicious-tarballs (off by default): ALSO downloads each tarball, which
is KNOWN MALWARE, lists its members in memory (never extracts or executes), and
records whether a root binding.gyp exists and its size. This is how the
2026-10-01 record was produced; recorded for audit, not for reproduction.
"""
import argparse, base64, collections, hashlib, io, json, pathlib, tarfile, urllib.parse, urllib.request

RAW = pathlib.Path(__file__).parent / "raw"
ap = argparse.ArgumentParser()
ap.add_argument("--fetch-malicious-tarballs", action="store_true", default=False)
args = ap.parse_args()

scan = json.loads((RAW / "jag_scan.json").read_text())
burst = [r for r in scan if "2026-06-04T00:25" <= r["time"] < "2026-06-04T00:31" and r["present"]]
pk_cache, rows = {}, []
for r in burst:
    n, v = r["pkg"], r["ver"]
    if n not in pk_cache:
        with urllib.request.urlopen("https://registry.npmjs.org/" + urllib.parse.quote(n, safe="@"), timeout=30) as f:
            pk_cache[n] = json.loads(f.read())
    meta = pk_cache[n]["versions"][v]
    integ = meta["dist"]["integrity"]
    assert integ.startswith("sha512-")
    integ_hex = base64.b64decode(integ[len("sha512-"):]).hex()
    att = json.loads((RAW / f"jag_att_{n.replace('/', '_')}_{v}.json").read_text())
    subj = None
    for a in att["attestations"]:
        if a["predicateType"] == "https://slsa.dev/provenance/v1":
            p = json.loads(base64.b64decode(a["bundle"]["dsseEnvelope"]["payload"]))
            subj = p["subject"][0]["digest"]["sha512"]
    row = {"pkg": n, "ver": v, "deprecated": bool(meta.get("deprecated")),
           "integrity_matches_attestation": subj == integ_hex}
    if args.fetch_malicious_tarballs:
        with urllib.request.urlopen(meta["dist"]["tarball"], timeout=60) as f:
            data = f.read()
        row["tarball_sha512_matches_attestation"] = hashlib.sha512(data).hexdigest() == subj
        tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
        row["binding_gyp_sizes"] = [m.size for m in tf.getmembers()
                                    if m.name.rstrip("/").split("/")[-1] == "binding.gyp" and m.name.count("/") == 1]
    rows.append(row)

(RAW / "jag_gypcheck.json").write_text(json.dumps(rows, indent=1))
print("checked", len(rows))
print("deprecated:", sum(x["deprecated"] for x in rows))
print("dist.integrity matches attestation subject:", sum(x["integrity_matches_attestation"] for x in rows))
if args.fetch_malicious_tarballs:
    print("tarball sha512 matches attestation subject:", sum(x["tarball_sha512_matches_attestation"] for x in rows))
    print("root binding.gyp present:", sum(bool(x["binding_gyp_sizes"]) for x in rows))
    print("sizes:", collections.Counter(s for x in rows for s in x["binding_gyp_sizes"]))
