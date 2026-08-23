# Trivy ignore policy
# Source: https://williamzujkowski.github.io/posts/2025-10-06-automated-security-scanning-pipeline/
# Usage: trivy image --ignore-policy ./policy/security.rego myapp:latest
#
# READ THIS BEFORE WRITING A TRIVY POLICY.
#
# The flag is --ignore-policy. There is no --policy flag for this. And the name
# is the semantics: a Trivy Rego policy FILTERS FINDINGS OUT. It cannot deny,
# block, or fail a build. A policy written as "deny on critical" is, under the
# only mechanism Trivy offers, either inert or a rule that SUPPRESSES criticals
# — the opposite of what its author intended.
#
# Two further requirements that make a wrong policy silently no-op:
#   1. The rule MUST be named `ignore`. A `deny` or `warn` rule is never
#      evaluated.
#   2. `input` is a SINGLE DetectedVulnerability object, not a collection.
#      Iterating `input.Vulnerabilities[_]` never matches anything.
#
# To actually fail a build on severity, do not use Rego at all:
#   trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest

package trivy

default ignore = false

# Ignore unfixed findings below high severity. There is nothing to action on an
# unfixed low, and leaving them in the report is how people stop reading it.
ignore {
	input.Severity == "LOW"
	input.FixedVersion == ""
}

ignore {
	input.Severity == "MEDIUM"
	input.FixedVersion == ""
}

# Ignore a specific vulnerability with a recorded justification.
ignore {
	input.VulnerabilityID == "CVE-2024-12345"
}

# Ignore findings in a package that is present but not reachable at runtime.
ignore {
	input.PkgName == "example-package"
	input.Severity != "CRITICAL"
}
