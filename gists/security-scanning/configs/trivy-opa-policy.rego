# Trivy OPA Policy for Security Scanning
# Source: https://williamzujkowski.github.io/posts/2025-10-06-automated-security-scanning-pipeline/
# Purpose: Define security policies using Open Policy Agent (OPA)
# Usage: Save as policy/security.rego and reference with trivy --policy

package trivy

# Deny images with critical vulnerabilities
deny[msg] {
    input.Vulnerabilities[_].Severity == "CRITICAL"
    msg := sprintf("Critical vulnerability found: %s", [input.Vulnerabilities[_].VulnerabilityID])
}

# Deny specific packages
deny[msg] {
    input.Packages[_].Name == "log4j"
    input.Packages[_].Version < "2.17.0"
    msg := "Log4j version < 2.17.0 detected (Log4Shell vulnerability)"
}

# Warn on high severity
warn[msg] {
    input.Vulnerabilities[_].Severity == "HIGH"
    msg := sprintf("High severity vulnerability: %s", [input.Vulnerabilities[_].VulnerabilityID])
}
