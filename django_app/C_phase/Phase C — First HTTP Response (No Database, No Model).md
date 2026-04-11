# Phase C — First HTTP Response (No Database, No Model)

## What you did

### 1. Add the health view in `tasks/views.py`

```python
from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok"})
```

`JsonResponse` sets `Content-Type: application/json` automatically and serializes the dict.

---

### 2. Wire the view into `config/urls.py`

```python
from django.contrib import admin
from django.urls import path

from tasks.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
]
```

The second argument to `path()` is the view callable itself — no quotes.

---

### 3. Start the dev server and verify

```bash
uv run python manage.py runserver 0.0.0.0:8000
```

`0.0.0.0` binds to all interfaces inside the container so the port is reachable from outside.

```bash
curl http://localhost:8000/health/
```

**Expected response:**

```json
{"status": "ok"}
```

---

## To repeat Phase C from scratch

1. Edit `tasks/views.py` — add the `health` function
2. Edit `config/urls.py` — import `health` and add `path("health/", health)`
3. `uv run python manage.py runserver 0.0.0.0:8000`
4. `curl http://localhost:8000/health/` — verify `{"status": "ok"}`

---

## Phase C — End state

| What exists | Status |
|---|---|
| `health` view function | ✅ |
| URL wired to view | ✅ |
| Dev server running | ✅ |
| Full request cycle verified | ✅ |
| Task model | ❌ Phase D |
| Task URLs and views | ❌ Phase E |
