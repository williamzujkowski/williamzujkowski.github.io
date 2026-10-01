"""For every still-present burst version in jag_scan.json, list tarball members
(no extraction) and record whether a root binding.gyp exists and its size, and
whether the version carries an npm deprecation notice. Also check that the
tarball sha512 equals the attestation subject digest."""
import json, urllib.request, urllib.parse, tarfile, io, hashlib, base64, pathlib, collections

RAW = pathlib.Path(__file__).parent / "raw"
scan = json.loads((RAW / "jag_scan.json").read_text())
burst = [r for r in scan if "2026-06-04T00:25" <= r["time"] < "2026-06-04T00:31" and r["present"]]
pk_cache = {}
rows = []
for r in burst:
    n, v = r["pkg"], r["ver"]
    if n not in pk_cache:
        with urllib.request.urlopen("https://registry.npmjs.org/" + urllib.parse.quote(n, safe="@"), timeout=30) as f:
            pk_cache[n] = json.loads(f.read())
    meta = pk_cache[n]["versions"][v]
    with urllib.request.urlopen(meta["dist"]["tarball"], timeout=60) as f:
        data = f.read()
    sha512_hex = hashlib.sha512(data).hexdigest()
    att = json.loads((RAW / f"jag_att_{n.replace('/', '_')}_{v}.json").read_text())
    subj = None
    for a in att["attestations"]:
        if a["predicateType"] == "https://slsa.dev/provenance/v1":
            p = json.loads(base64.b64decode(a["bundle"]["dsseEnvelope"]["payload"]))
            subj = p["subject"][0]["digest"]["sha512"]
    tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
    gyp = [m.size for m in tf.getmembers() if m.name.rstrip("/").split("/")[-1] == "binding.gyp" and m.name.count("/") == 1]
    rows.append({"pkg": n, "ver": v, "binding_gyp_sizes": gyp, "deprecated": bool(meta.get("deprecated")),
                 "digest_matches_attestation": subj == sha512_hex})
(RAW / "jag_gypcheck.json").write_text(json.dumps(rows, indent=1))
print("checked", len(rows))
print("root binding.gyp present:", sum(bool(x["binding_gyp_sizes"]) for x in rows))
print("sizes:", collections.Counter(s for x in rows for s in x["binding_gyp_sizes"]))
print("deprecated:", sum(x["deprecated"] for x in rows))
print("digest matches attestation subject:", sum(x["digest_matches_attestation"] for x in rows))
