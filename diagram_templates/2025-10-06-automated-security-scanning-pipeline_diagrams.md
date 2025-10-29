# Diagrams for 2025-10-06-automated-security-scanning-pipeline.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown
4. Extract large code blocks (58+ lines) to GitHub gists

---

## Security Scanning Architecture

```mermaid
graph TB
    subgraph "Input Sources"
        Docker[Docker Images]
        SBOM[SBOM Files]
        Repo[Git Repositories]
    end

    subgraph "Grype Scanner"
        GImg[Image Scan]
        GDB[Vulnerability Database]
        GMatch[Pattern Matching]
        GReport[Grype Results]
    end

    subgraph "OSV Scanner"
        OSVScan[OSV Scan]
        OSVDB[(OSV Database)]
        OSVMatch[Dependency Check]
        OSVReport[OSV Results]
    end

    subgraph "Wazuh Integration"
        Parse[Result Parser]
        Transform[Data Transformer]
        WazuhAPI[Wazuh API]
        SIEM[Wazuh SIEM]
    end

    subgraph "Alerting & Response"
        Alert[Alert Generator]
        Ticket[Ticket Creation]
        Dashboard[Dashboard]
    end

    Docker --> GImg
    SBOM --> GImg
    Repo --> OSVScan

    GImg --> GDB
    GDB --> GMatch
    GMatch --> GReport

    OSVScan --> OSVDB
    OSVDB --> OSVMatch
    OSVMatch --> OSVReport

    GReport --> Parse
    OSVReport --> Parse
    Parse --> Transform
    Transform --> WazuhAPI
    WazuhAPI --> SIEM

    SIEM --> Alert
    Alert --> Ticket
    SIEM --> Dashboard

    style GImg fill:#ff9800
    style OSVScan fill:#2196f3
    style WazuhAPI fill:#4caf50
    style SIEM fill:#9c27b0
    style Alert fill:#f44336
```

## Scanning Workflow

```mermaid
flowchart TD
    Start([CI/CD Trigger]) --> CheckType{Scan Type?}

    CheckType -->|Container| PrepDocker[Prepare Docker Image]
    CheckType -->|Code| PrepRepo[Clone Repository]

    PrepDocker --> RunGrype[Run Grype Scan]
    PrepRepo --> RunOSV[Run OSV Scan]

    RunGrype --> ParseG{Vulnerabilities<br/>Found?}
    RunOSV --> ParseO{Vulnerabilities<br/>Found?}

    ParseG -->|Yes| FilterCrit{Critical/High<br/>Severity?}
    ParseG -->|No| PassG[Mark Pass]

    ParseO -->|Yes| FilterCVSS{CVSS >= 7.0?}
    ParseO -->|No| PassO[Mark Pass]

    FilterCrit -->|Yes| SendWazuh[Send to Wazuh]
    FilterCrit -->|No| LogWarn[Log Warning]

    FilterCVSS -->|Yes| SendWazuh
    FilterCVSS -->|No| LogWarn

    SendWazuh --> CreateAlert[Create Alert]
    CreateAlert --> AutoTicket{Auto-ticket<br/>Enabled?}

    AutoTicket -->|Yes| CreateJira[Create Jira Ticket]
    AutoTicket -->|No| NotifyTeam[Notify Team]

    CreateJira --> UpdateDB[Update Vuln DB]
    NotifyTeam --> UpdateDB
    LogWarn --> UpdateDB
    PassG --> UpdateDB
    PassO --> UpdateDB

    UpdateDB --> End([Complete])

    style RunGrype fill:#ff9800
    style RunOSV fill:#2196f3
    style SendWazuh fill:#4caf50
    style CreateAlert fill:#f44336
    style CreateJira fill:#9c27b0
```

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant CI as CI/CD Pipeline
    participant Grype as Grype Scanner
    participant OSV as OSV Scanner
    participant Parser as Result Parser
    participant Wazuh as Wazuh SIEM
    participant Jira as Jira API

    CI->>Grype: Scan Docker image
    activate Grype
    Grype->>Grype: Query vulnerability DB
    Grype-->>CI: Return CVE results
    deactivate Grype

    CI->>OSV: Scan dependencies
    activate OSV
    OSV->>OSV: Check OSV database
    OSV-->>CI: Return vulnerability results
    deactivate OSV

    CI->>Parser: Send combined results
    activate Parser
    Parser->>Parser: Filter by severity
    Parser->>Parser: Transform to MITRE format
    Parser-->>Wazuh: Push alert data
    deactivate Parser

    activate Wazuh
    Wazuh->>Wazuh: Create alert
    Wazuh->>Wazuh: Correlate events
    Wazuh-->>Jira: Auto-create ticket
    deactivate Wazuh

    activate Jira
    Jira->>Jira: Assign to team
    Jira-->>CI: Return ticket ID
    deactivate Jira
```

## Severity Classification

```mermaid
graph LR
    subgraph "Input"
        CVE[CVE/Advisory]
    end

    subgraph "Scoring"
        CVSS[CVSS Score]
        EPSS[EPSS Score]
        KEV{In KEV<br/>Catalog?}
    end

    subgraph "Classification"
        Critical[Critical: CVSS>=9 OR KEV]
        High[High: CVSS 7-8.9]
        Medium[Medium: CVSS 4-6.9]
        Low[Low: CVSS <4]
    end

    subgraph "Action"
        Block[Block Deployment]
        Review[Require Review]
        Monitor[Monitor Only]
        Info[Info Only]
    end

    CVE --> CVSS
    CVE --> EPSS
    CVE --> KEV

    CVSS --> Critical
    KEV -->|Yes| Critical
    CVSS --> High
    CVSS --> Medium
    CVSS --> Low

    Critical --> Block
    High --> Review
    Medium --> Monitor
    Low --> Info

    style Critical fill:#f44336
    style High fill:#ff9800
    style Medium fill:#ffc107
    style Low fill:#4caf50
    style Block fill:#d32f2f
    style Review fill:#f57c00
```

## Usage Example

Replace this verbose code:
```python
# 58 lines of scanner configuration code
```

With:
```python
# Essential config only (5-10 lines)
scanner = VulnScanner(
    grype_db="/var/lib/grype",
    osv_cache="/var/cache/osv",
    wazuh_endpoint="https://wazuh.local:55000"
)
scanner.scan_image("myapp:latest")
# Full config: https://gist.github.com/...
```

And add architecture diagram above the code.
