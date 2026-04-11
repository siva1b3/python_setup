flowchart TD
Client["HTTP Request\n(browser / curl / React)"]

    subgraph config["config/ (project level)"]
        URLS["urls.py\nproject router"]
    end

    subgraph tasks["tasks/ (app level)"]
        TURLS["urls.py\napp router\n(created in Step 27)"]
        VIEWS["views.py\nview function"]
        MODELS["models.py\nORM / database queries"]
    end

    DB[(PostgreSQL)]

    Client --> URLS
    URLS -->|"includes tasks.urls\n(Step 27)"| TURLS
    TURLS --> VIEWS
    VIEWS --> MODELS
    MODELS --> DB
    DB --> MODELS
    MODELS --> VIEWS
    VIEWS -->|"HttpResponse / JsonResponse"| Client

    style config fill:#1e3a5f,stroke:#4a90d9
    style tasks fill:#1e4a2e,stroke:#4aaa6a
    style DB fill:#4a2000,stroke:#cc7700
