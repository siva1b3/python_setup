## What I did in Step 0 (minor deviations from the plan)

- **Package manager:** Using `uv` instead of `pip` + `requirements.txt`. So `pyproject.toml` + `uv.lock` + `.python-version` replace the plan's `requirements.txt`. Carry this forward to all Python components.
- **Folder layout:** Using flat per-step folders at the repo root (e.g. `a_step_0/`) instead of the plan's `src/simulator/`, `src/api/` monorepo tree.
- **Compose files:** One `docker-compose.dev.yml` for development (not split into `app.yml` + `infra.yml` yet) plus `docker-compose.network.yml` and `docker-compose.prod.yml`.

### Step 0 folder

```
a_step_0/
├── .python-version
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.network.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── simulator.py
└── README.md
```