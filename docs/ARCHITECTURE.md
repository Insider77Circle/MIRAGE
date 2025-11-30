# Mirage V3 Architecture

This document outlines the high-level architecture of the Mirage V3 honeypot system.

## Component Diagram

The diagram below illustrates the flow of data from an external user/attacker through the backend systems and to the front-end user interface.

```mermaid
graph TD
    subgraph "External World"
        A[User / Attacker]
        UI_User[Admin User]
    end

    subgraph "Mirage V3 Backend (on Server)"
        LP[Honeypot TCP Ports <br> 21, 22, 80, 443, 8080]
        
        subgraph "Core Logic (mirage_core.py)"
            HC[handle_client <br> Raw TCP Handler]
            MAI[MirageAI <br> AI Kernel]
            FAB[Fabricator <br> Asset Generator]
        end

        subgraph "Web Interface (web_server.py)"
            WS[aiohttp Web Server <br> on Port 8081]
            WSH[WebSocket Handler]
        end

        LLM[External LLM API <br> e.g., Moonshot]
    end

    subgraph "User Interface"
        UI[Web UI <br> index.html]
    end

    %% Connections
    A --> LP
    LP --> HC
    HC --> MAI
    MAI --> LLM
    LLM --> MAI
    MAI --> HC

    HC -- "Sends Events (Connections, Logs)" --> WSH

    UI_User --> WS
    WS -- "Serves index.html" --> UI
    UI -- "Connects" --> WSH
    WSH -- "Broadcasts Events" --> UI
    
    %% Style Definitions
    classDef backend fill:#2a2a3e,stroke:#8c71d9,stroke-width:2px,color:#fff;
    classDef core fill:#1c1c2b,stroke:#a38ee6,stroke-width:1px,color:#fff;
    classDef web fill:#1c1c2b,stroke:#a38ee6,stroke-width:1px,color:#fff;
    classDef external fill:#4a4a6a,stroke:#b3a2e8,stroke-width:2px,color:#fff;

    class MAI,HC,FAB,WS,WSH,LP,LLM backend;
    class A,UI_User external;
```