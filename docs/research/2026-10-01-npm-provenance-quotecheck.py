"""Fetch each cited page and confirm each quoted phrase appears verbatim (after
whitespace/HTML normalisation). Prints FOUND/MISSING per phrase."""
import re, html, urllib.request, json, pathlib

CHECKS = {
    "https://slsa.dev/spec/v1.2/threats": ["cannot be directly mitigated through SLSA controls"],
    "https://slsa.dev/spec/v1.0/threats": [
        "does not reflect the intent of the software producer",
        "SLSA v1.0 does not address source threats",
        "SLSA v1.0 does not address this threat"],
    "https://docs.npmjs.com/generating-provenance-statements": [
        "does not guarantee the package has no malicious code",
        "a verifiable link to the package's source code and build instructions"],
    "https://www.endorlabs.com/learn/npm-malware-compromises-keyv-and-cacheable-with-500m-weekly-downloads-and-spreads-to-hundreds-of-packages": [
        "through the project's legitimate GitHub Actions OIDC trusted publishing pipeline after a commit to",
        "valid npm signatures and SLSA provenance"],
    "https://socket.dev/blog/popular-npm-packages-in-the-keyv-and-cacheable-namespaces-compromised-in-active-supply-chain": [
        "provenance attests build integrity, not source integrity"],
    "https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm": ["157", "binding.gyp", "jagreehal"],
    "https://www.stepsecurity.io/blog/injective-npm-supply-chain-attack-18-packages-backdoored-to-steal-crypto-wallet-keys": [
        "5486f13e799d9c90095c5f581a04ad867d768f66", "publish.yaml"],
    "https://corgea.com/research/redhat-cloud-services-npm-miasma-shai-hulud-worm": ["orphan", "filename"],
    "https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7": ["compromised npm publish token"],
    "https://docs.npmjs.com/trusted-publishers": ["Workflow filename (required)", "Environment name (optional)"],
    "https://docs.npmjs.com/staged-publishing": ["two-factor authentication (2FA)", "npm stage publish"],
}

def norm(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t)

res = {}
for url, phrases in CHECKS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read().decode("utf-8", "replace")
        t = norm(raw)
        # also search raw (JSON-embedded content in some SPA pages)
        r2 = html.unescape(raw).replace("\\u0027", "'")
        for p in phrases:
            ok = p in t or p in r2
            res[f"{url} :: {p}"] = ok
            print("FOUND  " if ok else "MISSING", url[:70], "::", p)
    except Exception as e:
        print("ERROR  ", url, e)
pathlib.Path(__file__).with_name("quotecheck.json").write_text(json.dumps(res, indent=1))
