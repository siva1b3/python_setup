# Django + DRF Learning Roadmap — Progress Summary

## Phase A — Python project and Django bootstrap

---

### Step 1 — Install Django and DRF
```
uv add django djangorestframework
```
Installs Django and DRF into the environment. After this, `import django` and `import rest_framework` both work.

---

### Step 2 — Freeze dependencies *(skipped)*
Not needed — `uv` manages `pyproject.toml` and `uv.lock` automatically.

---

### Step 3 — Create the Django project
```
uv run django-admin startproject config .
```
The trailing dot places `manage.py` and `config/` in the current directory.

**Result:**
```
manage.py
config/
    __init__.py
    settings.py
    urls.py
    wsgi.py
    asgi.py
```

---

### Step 4 — Project layout (theory)

| File | Purpose |
|---|---|
| `manage.py` | CLI entry point for all Django commands |
| `config/settings.py` | Central configuration — edited in almost every step |
| `config/urls.py` | Top-level URL routing entry point |
| `config/wsgi.py` | Production server interface (Gunicorn) |
| `config/asgi.py` | Async production server interface (Uvicorn) |

Common commands via `manage.py`:
```
uv run python manage.py runserver
uv run python manage.py migrate
uv run python manage.py makemigrations
uv run python manage.py shell
```

---

### Step 5 — Create the tasks app
```
uv run python manage.py startapp tasks
```

**Result:**
```
tasks/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    tests.py
    migrations/
        __init__.py
```

---

### Step 6 — App layout and project-vs-app distinction (theory)

| Concept | Project | App |
|---|---|---|
| What it is | Entire deployable unit | One self-contained feature module |
| How many | One per codebase | Many per project |
| Contains | Settings, top-level URLs | Models, views, migrations for one feature |

> **Rule:** Feature code always goes inside an app, never inside `config/`.

---

### Step 7 — `INSTALLED_APPS` (theory)

Django does not auto-scan for apps. You must register every app explicitly.

When Django starts, for each app in `INSTALLED_APPS` it:
1. Imports `models.py` and registers all models with the ORM
2. Includes `migrations/` in the migration graph
3. Loads app configuration from `apps.py`

**Silent failure trap:** If your app is not registered, `makemigrations` outputs "No changes detected" with no error.
---

### Step 8 — Register `tasks` in `INSTALLED_APPS`

`config/settings.py`:
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]
```

Verify:
```
uv run python manage.py check
# Expected: System check identified no issues (0 silenced).
```

---

### Step 9 — Register `rest_framework` in `INSTALLED_APPS`

`config/settings.py`:
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",   # third-party apps go here
    "tasks",            # your own apps go last
]
```

**Order convention:** built-in Django apps → third-party apps → your own apps.

Verify:
```
uv run python manage.py check
# Expected: System check identified no issues (0 silenced).
```

---

## Phase A Complete ✅

| What exists | Status |
|---|---|
| Django + DRF installed | ✅ |
| Project structure created | ✅ |
| `tasks` app created | ✅ |
| Both apps registered | ✅ |
| Database connected | ❌ Phase B |
| Any URL or view | ❌ Phase C |

---
