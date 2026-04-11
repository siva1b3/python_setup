# Phase E — Plain Django JSON Views for Reading Data

## What you did

### 1. Theory — `Task.objects.all()` and QuerySets (Step 23)

`Task.objects.all()` returns a **QuerySet** — a lazy description of a database query. Django only executes the SQL when you consume the QuerySet: iterate over it, pass it to `list()`, or access its length.

You can chain filters before any SQL runs:

```python
Task.objects.all().filter(done=False)
```

Django combines the conditions into a single SQL query. `Task.objects` is the default **Manager** — the interface between the model class and the database.

---

### 2. Replace hardcoded view with `task_list` (Step 24)

**`tasks/views.py`:**

```python
from django.http import JsonResponse
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


def task_list(request):
    tasks = Task.objects.all()
    data = [
        {
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        }
        for task in tasks
    ]
    return JsonResponse(data, safe=False)
```

`safe=False` is required because the top-level value is a list, not a dict.

**`config/urls.py`:**

```python
from django.contrib import admin
from django.urls import path
from tasks.views import health, task_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("tasks/", task_list),
]
```

---

### 3. Add `task_detail` view (Step 25)

Add to `tasks/views.py`:

```python
def task_detail(request, task_id):
    task = Task.objects.get(task_id=task_id)
    data = {
        "task_id": task.task_id,
        "title": task.title,
        "done": task.done,
    }
    return JsonResponse(data)
```

Add to `config/urls.py`:

```python
from tasks.views import health, task_list, task_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("tasks/", task_list),
    path("tasks/<int:task_id>/", task_detail),
]
```

`<int:task_id>` captures the integer from the URL and passes it as the `task_id` argument to the view.

---

### 4. Handle "task not found" with a 404 JSON response (Step 26)

Update `task_detail` in `tasks/views.py`:

```python
def task_detail(request, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    data = {
        "task_id": task.task_id,
        "title": task.title,
        "done": task.done,
    }
    return JsonResponse(data)
```

`Task.DoesNotExist` is raised by `get()` when no matching row is found. Without this, Django returns an HTML error page — not acceptable for an API.

---

### 5. Split tasks URLs into `tasks/urls.py` (Step 27)

**Create `tasks/urls.py`:**

```python
from django.urls import path
from tasks.views import task_list, task_detail

urlpatterns = [
    path("", task_list),
    path("<int:task_id>/", task_detail),
]
```

The `tasks/` prefix is removed here — it is handled by `config/urls.py`.

**Final `config/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include
from tasks.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("tasks/", include("tasks.urls")),
]
```

---

## To repeat Phase E from scratch

1. Edit `tasks/views.py` — add `task_list` and `task_detail` functions
2. Edit `config/urls.py` — add `path("tasks/", task_list)` and `path("tasks/<int:task_id>/", task_detail)`
3. Verify: `curl http://localhost:8000/tasks/` and `curl http://localhost:8000/tasks/1/`
4. Add `try/except Task.DoesNotExist` to `task_detail`
5. Verify 404: `curl -i http://localhost:8000/tasks/999/`
6. Create `tasks/urls.py` — move task URL patterns into it
7. Edit `config/urls.py` — replace task paths with `path("tasks/", include("tasks.urls"))`
8. Verify all endpoints still work

---

## Final file state

**`tasks/views.py`:**

```python
from django.http import JsonResponse
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


def task_list(request):
    tasks = Task.objects.all()
    data = [
        {
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        }
        for task in tasks
    ]
    return JsonResponse(data, safe=False)


def task_detail(request, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    data = {
        "task_id": task.task_id,
        "title": task.title,
        "done": task.done,
    }
    return JsonResponse(data)
```

**`tasks/urls.py`:**

```python
from django.urls import path
from tasks.views import task_list, task_detail

urlpatterns = [
    path("", task_list),
    path("<int:task_id>/", task_detail),
]
```

**`config/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include
from tasks.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("tasks/", include("tasks.urls")),
]
```

---

## Phase E — End state

| What exists | Status |
|---|---|
| `task_list` view (GET all tasks) | ✅ |
| `task_detail` view (GET single task) | ✅ |
| 404 JSON response for missing task | ✅ |
| Tasks URL split into `tasks/urls.py` | ✅ |
| Write views (POST, PUT, DELETE) | ❌ Phase F |
| DRF views | ❌ Phase G |
