"""Save the SLSA provenance Sigstore bundle from an npm attestation response and
print the Fulcio certificate SAN + GitHub-specific extensions."""
import json, sys, base64, pathlib
from cryptography import x509

RAW = pathlib.Path(__file__).parent / "raw"
OIDS = {
    "1.3.6.1.4.1.57264.1.8": "Issuer (V2)",
    "1.3.6.1.4.1.57264.1.9": "Build Signer URI",
    "1.3.6.1.4.1.57264.1.11": "Runner Environment",
    "1.3.6.1.4.1.57264.1.12": "Source Repository URI",
    "1.3.6.1.4.1.57264.1.13": "Source Repository Digest",
    "1.3.6.1.4.1.57264.1.14": "Source Repository Ref",
    "1.3.6.1.4.1.57264.1.18": "Build Config URI",
    "1.3.6.1.4.1.57264.1.20": "Build Trigger",
    "1.3.6.1.4.1.57264.1.21": "Run Invocation URI",
    "1.3.6.1.4.1.57264.1.22": "Source Repository Visibility At Signing",
}

for fn in sys.argv[1:]:
    data = json.loads((RAW / fn).read_text())
    for a in data["attestations"]:
        if a["predicateType"] != "https://slsa.dev/provenance/v1":
            continue
        b = a["bundle"]
        out = RAW / fn.replace("att_", "bundle_")
        out.write_text(json.dumps(b))
        vm = b["verificationMaterial"]
        raw = vm.get("certificate", {}).get("rawBytes") or vm["x509CertificateChain"]["certificates"][0]["rawBytes"]
        cert = x509.load_der_x509_certificate(base64.b64decode(raw))
        print("==", fn, "mediaType", b.get("mediaType"))
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        print(" SAN:", [str(u) for u in san.get_values_for_type(x509.UniformResourceIdentifier)])
        print(" notBefore:", cert.not_valid_before_utc)
        for ext in cert.extensions:
            o = ext.oid.dotted_string
            if o in OIDS:
                v = ext.value.value
                # V2 extensions are DER UTF8String: strip 2-byte tag/len header
                s = v[2:].decode(errors="replace") if v[:1] == b"\x0c" else v.decode(errors="replace")
                print(f"  {OIDS[o]}: {s}")
        tl = vm.get("tlogEntries", [{}])[0]
        print(" rekor logIndex:", tl.get("logIndex"), "integratedTime:", tl.get("integratedTime"))
