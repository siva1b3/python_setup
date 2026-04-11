# Phase A — Python Project and Django Bootstrap

## What you did

### 1. Install Django and DRF
```bash
uv add django djangorestframework
```
`uv` manages `pyproject.toml` and `uv.lock` automatically — no manual `pip freeze` needed.

---

### 2. Create the Django project
```bash
uv run django-admin startproject config .
```
Trailing dot places `manage.py` and `config/` in the current directory.

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

### 3. Create the tasks app
```bash
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

### 4. Register apps in `config/settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",   # third-party apps
    "tasks",            # your own apps last
]
```

Order convention: built-in Django apps → third-party apps → your own apps.

---

### 5. Verify
```bash
uv run python manage.py check
# Expected: System check identified no issues (0 silenced).
```

---

## To repeat Phase A from scratch

1. `uv add django djangorestframework`
2. `uv run django-admin startproject config .`
3. `uv run python manage.py startapp tasks`
4. Edit `config/settings.py` — add `"rest_framework"` and `"tasks"` to `INSTALLED_APPS`
5. `uv run python manage.py check`

---

## Phase A — End state

| What exists | Status |
|---|---|
| Django + DRF installed | ✅ |
| Project structure created | ✅ |
| `tasks` app created | ✅ |
| Both apps registered | ✅ |
| Database connected | ❌ Phase B |
| Any URL or view | ❌ Phase C |
