# Diagrams for 2025-09-14-threat-intelligence-mitre-attack-dashboard.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown
4. Extract large code blocks (42+ lines) to GitHub gists

---

## MITRE ATT&CK Dashboard Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        MITRE[MITRE ATT&CK<br/>API]
        Wazuh[Wazuh SIEM<br/>Alerts]
        OSQuery[OSQuery<br/>Events]
        Custom[Custom Feeds]
    end

    subgraph "ETL Pipeline"
        Fetch[Data Fetcher]
        Parse[JSON Parser]
        Map[Technique Mapper]
        Enrich[Context Enricher]
        Cache[(Redis Cache)]
    end

    subgraph "Dashboard Backend"
        API[REST API]
        QueryEngine[Query Engine]
        Analytics[Analytics Engine]
        DB[(PostgreSQL)]
    end

    subgraph "Frontend"
        Matrix[ATT&CK Matrix View]
        Timeline[Timeline View]
        Search[Search Interface]
        Export[Export Tools]
    end

    MITRE --> Fetch
    Wazuh --> Fetch
    OSQuery --> Fetch
    Custom --> Fetch

    Fetch --> Parse
    Parse --> Map
    Map --> Enrich
    Enrich --> Cache
    Cache --> DB

    DB --> QueryEngine
    QueryEngine --> API
    Analytics --> API

    API --> Matrix
    API --> Timeline
    API --> Search
    API --> Export

    style MITRE fill:#2196f3
    style Wazuh fill:#4caf50
    style API fill:#ff9800
    style Matrix fill:#9c27b0
```

## Data Ingestion Workflow

```mermaid
flowchart TD
    Start([Scheduled Run]) --> CheckCache{Cache<br/>Valid?}

    CheckCache -->|Yes| LoadCache[Load from Cache]
    CheckCache -->|No| FetchMITRE[Fetch MITRE Data]

    FetchMITRE --> ParseJSON[Parse JSON Response]
    ParseJSON --> ExtractTech[Extract Techniques]

    ExtractTech --> MapTactics[Map to Tactics]
    MapTactics --> EnrichData[Enrich with Context]

    EnrichData --> FetchEvents[Fetch SIEM Events]
    FetchEvents --> CorrelateEvents[Correlate Events<br/>to Techniques]

    CorrelateEvents --> CalcStats[Calculate Statistics]
    CalcStats --> GenerateMatrix[Generate Matrix View]

    GenerateMatrix --> UpdateDB[Update Database]
    LoadCache --> UpdateDB

    UpdateDB --> UpdateCache[Update Cache]
    UpdateCache --> NotifyClients[Notify WebSocket Clients]

    NotifyClients --> End([Complete])

    style FetchMITRE fill:#2196f3
    style CorrelateEvents fill:#4caf50
    style GenerateMatrix fill:#9c27b0
    style UpdateCache fill:#ff9800
```

## API Request Flow

```mermaid
sequenceDiagram
    participant Client as Web Client
    participant LB as Load Balancer
    participant API as Dashboard API
    participant Cache as Redis Cache
    participant DB as PostgreSQL
    participant MITRE as MITRE API

    Client->>LB: GET /api/matrix
    activate LB
    LB->>API: Forward request
    deactivate LB

    activate API
    API->>Cache: Check cache
    activate Cache

    alt Cache hit
        Cache-->>API: Return cached data
    else Cache miss
        Cache-->>API: Cache miss
        API->>DB: Query techniques
        activate DB
        DB-->>API: Return techniques
        deactivate DB

        API->>MITRE: Fetch latest updates
        activate MITRE
        MITRE-->>API: Return updates
        deactivate MITRE

        API->>API: Merge & enrich data
        API->>Cache: Update cache
    end

    deactivate Cache
    API-->>Client: Return matrix data
    deactivate API

    Client->>Client: Render visualization
```

## Technique Mapping Process

```mermaid
graph TB
    subgraph "Input Events"
        SysLog[System Logs]
        NetFlow[Network Traffic]
        ProcEvents[Process Events]
        FileEvents[File Events]
    end

    subgraph "Pattern Matching"
        Regex[Regex Patterns]
        Heuristics[Heuristic Rules]
        ML[ML Model]
    end

    subgraph "MITRE Mapping"
        TechID[Technique ID]
        TacticID[Tactic ID]
        SubTech[Sub-technique]
    end

    subgraph "Enrichment"
        AddContext[Add Context]
        CalcScore[Calculate Score]
        Classify[Classify Severity]
    end

    subgraph "Output"
        Alert[Alert Entry]
        Dashboard[Dashboard Update]
        Report[Report Entry]
    end

    SysLog --> Regex
    NetFlow --> Heuristics
    ProcEvents --> ML
    FileEvents --> Regex

    Regex --> TechID
    Heuristics --> TechID
    ML --> TechID

    TechID --> TacticID
    TacticID --> SubTech

    SubTech --> AddContext
    AddContext --> CalcScore
    CalcScore --> Classify

    Classify --> Alert
    Classify --> Dashboard
    Classify --> Report

    style ML fill:#9c27b0
    style TechID fill:#2196f3
    style Alert fill:#f44336
```

## Dashboard Component Structure

```mermaid
graph LR
    subgraph "Frontend Components"
        Header[Header Bar]
        Sidebar[Sidebar Nav]
        Matrix[Matrix View]
        Timeline[Timeline View]
        Details[Details Panel]
    end

    subgraph "State Management"
        Store[Redux Store]
        Actions[Actions]
        Reducers[Reducers]
    end

    subgraph "Data Layer"
        APIClient[API Client]
        WS[WebSocket]
        LocalCache[Local Storage]
    end

    Header --> Store
    Sidebar --> Store
    Matrix --> Store
    Timeline --> Store
    Details --> Store

    Store --> Actions
    Actions --> Reducers
    Reducers --> Store

    APIClient --> Store
    WS --> Store
    Store --> LocalCache

    style Matrix fill:#9c27b0
    style Store fill:#ff9800
    style WS fill:#4caf50
```

## Usage Example

Replace this verbose code:
```python
# 42 lines of API setup and data fetching
```

With:
```python
# Essential setup only
dashboard = ATTACKDashboard(
    api_key=os.getenv("MITRE_API_KEY"),
    cache_ttl=3600
)
matrix_data = dashboard.get_matrix()
# Full implementation: https://gist.github.com/...
```

And add architecture diagram above the code.

## Coverage Heatmap Data Structure

```mermaid
graph TD
    subgraph "Coverage Calculation"
        DetectedEvents[Detected Events]
        AllTechniques[All MITRE Techniques]
        Calculate[Calculate Coverage %]
    end

    subgraph "Heatmap Generation"
        Normalize[Normalize to 0-100]
        ColorMap[Apply Color Scale]
        Render[Render Matrix]
    end

    subgraph "Color Scale"
        Zero[0%: Gray]
        Low[1-25%: Blue]
        Med[26-75%: Yellow]
        High[76-100%: Red]
    end

    DetectedEvents --> Calculate
    AllTechniques --> Calculate
    Calculate --> Normalize
    Normalize --> ColorMap

    ColorMap --> Zero
    ColorMap --> Low
    ColorMap --> Med
    ColorMap --> High

    Zero --> Render
    Low --> Render
    Med --> Render
    High --> Render

    style High fill:#f44336
    style Med fill:#ffc107
    style Low fill:#2196f3
    style Zero fill:#9e9e9e
```
