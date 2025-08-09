# Diagrams for 2025-06-25-local-llm-deployment-privacy-first.md

## How to use these diagrams:

1. Copy the Mermaid diagram code blocks
2. Replace verbose code sections in your blog post
3. The diagrams will render automatically in markdown

---


## Local LLM Architecture

```mermaid
graph TB
    subgraph "Hardware Layer"
        GPU[GPU/TPU]
        CPU[CPU]
        RAM[Memory]
        Storage[(Model Storage)]
    end
    
    subgraph "Model Layer"
        Llama[Llama 2]
        Mistral[Mistral]
        Custom[Fine-tuned]
    end
    
    subgraph "Inference Engine"
        GGML[GGML]
        ONNX[ONNX Runtime]
        TRT[TensorRT]
    end
    
    subgraph "API Layer"
        REST[REST API]
        WS[WebSocket]
        GRPC[gRPC]
    end
    
    subgraph "Applications"
        Web[Web UI]
        CLI[CLI Tool]
        Apps[Applications]
    end
    
    GPU --> GGML
    GPU --> TRT
    CPU --> ONNX
    
    Storage --> Llama
    Storage --> Mistral
    Storage --> Custom
    
    Llama --> GGML
    Mistral --> ONNX
    Custom --> TRT
    
    GGML --> REST
    ONNX --> WS
    TRT --> GRPC
    
    REST --> Web
    WS --> CLI
    GRPC --> Apps
    
    style GPU fill:#ff9800
    style GGML fill:#4caf50
    style REST fill:#2196f3
```

## LLM Request Processing

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant Q as Queue
    participant L as LLM Engine
    participant C as Cache
    participant M as Model
    
    U->>A: Send Prompt
    A->>C: Check Cache
    alt Cache Hit
        C-->>A: Cached Response
        A-->>U: Return Response
    else Cache Miss
        A->>Q: Queue Request
        Q->>L: Process Request
        L->>M: Load Model
        M-->>L: Model Ready
        L->>M: Generate Response
        M-->>L: Token Stream
        L->>C: Store in Cache
        L-->>A: Stream Response
        A-->>U: Stream to User
    end
```
