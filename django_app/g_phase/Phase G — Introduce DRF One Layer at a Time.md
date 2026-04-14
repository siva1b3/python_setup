# Phase G — Introduce DRF One Layer at a Time

## What you did

### Step 34 — Theory: Class-based views and why DRF uses them

No files change. The concept introduced is class-based views (CBVs) and why DRF builds on them instead of function-based views.

The Phase F views use `if request.method ==` branches inside a single function. As more methods are added, the function grows and all method logic is mixed in one block. There is no clean way to share setup code across methods without repeating it.

A class-based view maps each HTTP method to a class method — `get()`, `post()`, `put()`, `delete()`. Each method is isolated, readable, and independently testable. DRF's `APIView` extends Django's base CBV and adds `request.data` (auto-parsed body), `Response` (auto-serialized output), and `status` constants — replacing the three most repetitive manual steps from Phase F.

---

### Step 35 — Convert the list view to a DRF `APIView`

Replace the `task_list` function with a class `TaskListView` that extends `APIView`. Use DRF's `Response` and `status` instead of `JsonResponse` and hardcoded integers.

**`tasks/views.py`** — replace `task_list` function with `TaskListView` class:

```python
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        data = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "done": task.done,
            }
            for task in tasks
        ]
        return Response(data)

    def post(self, request):
        body = request.data
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return Response(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=status.HTTP_201_CREATED,
        )


@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    if request.method == "PUT":
        body = json.loads(request.body)
        task.title = body.get("title", task.title)
        task.done = body.get("done", task.done)
        task.save()
        return JsonResponse({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({}, status=204)
```

**`tasks/urls.py`** — update the list path to use `.as_view()`:

```python
from django.urls import path
from tasks.views import TaskListView, task_detail

urlpatterns = [
    path("", TaskListView.as_view()),
    path("<int:task_id>/", task_detail),
]
```

`.as_view()` converts the class into a callable that Django's URL router accepts.

**Test:**

```bash
# GET all tasks
curl -s http://localhost:8000/tasks/ | python -m json.tool

# POST new task
curl -s -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "DRF task"}' | python -m json.tool
```

---

### Step 36 — Convert the detail view to an `APIView` and use `get_object_or_404`

Replace the `task_detail` function with a class `TaskDetailView` that extends `APIView`. Use DRF's `get_object_or_404` instead of the manual `try/except Task.DoesNotExist` block.

**`tasks/views.py`** — replace `task_detail` function with `TaskDetailView` class:

```python
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        data = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "done": task.done,
            }
            for task in tasks
        ]
        return Response(data)

    def post(self, request):
        body = request.data
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return Response(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        return Response({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    def put(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        task.title = request.data.get("title", task.title)
        task.done = request.data.get("done", task.done)
        task.save()
        return Response({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    def delete(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

`import json` and `from django.views.decorators.csrf import csrf_exempt` are no longer needed — remove them.

**`tasks/urls.py`** — update the detail path:

```python
from django.urls import path
from tasks.views import TaskListView, TaskDetailView

urlpatterns = [
    path("", TaskListView.as_view()),
    path("<int:task_id>/", TaskDetailView.as_view()),
]
```

**Test:**

```bash
# GET single task
curl -s http://localhost:8000/tasks/1/ | python -m json.tool

# PUT update task
curl -s -X PUT http://localhost:8000/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | python -m json.tool

# DELETE task
curl -si -X DELETE http://localhost:8000/tasks/1/

# GET non-existent task — expect 404
curl -si http://localhost:8000/tasks/999/
```

---

### Step 37 — Confirm `@csrf_exempt` is gone and all four methods work

No new code is written. Confirm that `@csrf_exempt` is absent from both view classes and that all four HTTP methods work correctly through the `APIView` classes.

DRF's `APIView` uses `SessionAuthentication` by default, which handles CSRF internally for session-based clients. For all other authentication classes (including JWT which we add in Phase N), DRF skips the CSRF check entirely. So `@csrf_exempt` is not needed and must not be present.

**Verify all four methods:**

```bash
# GET list
curl -s http://localhost:8000/tasks/ | python -m json.tool

# POST create
curl -s -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test CSRF gone"}' | python -m json.tool

# PUT update — use the task_id returned from POST above
curl -s -X PUT http://localhost:8000/tasks/2/ \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | python -m json.tool

# DELETE
curl -si -X DELETE http://localhost:8000/tasks/2/
```

**Confirm in `tasks/views.py`:**
- No `import json`
- No `from django.views.decorators.csrf import csrf_exempt`
- No `@csrf_exempt` decorator anywhere
- Both `TaskListView` and `TaskDetailView` extend `APIView` cleanly

---

### Step 38 — Remove `@csrf_exempt` — DRF handles CSRF via authentication classes

No files change. This step formally closes Phase G.

`@csrf_exempt` is already absent. DRF's `APIView.as_view()` wraps the view with `csrf_exempt` internally when a non-session authentication class is active — you never write it yourself. For `SessionAuthentication`, DRF enforces CSRF correctly on its own. Either way, the decorator does not belong in your code.

---

## Final file state

**`tasks/views.py`:**

```python
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        data = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "done": task.done,
            }
            for task in tasks
        ]
        return Response(data)

    def post(self, request):
        body = request.data
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return Response(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        return Response({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    def put(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        task.title = request.data.get("title", task.title)
        task.done = request.data.get("done", task.done)
        task.save()
        return Response({
            "task_id": task.task_id,
            "title": task.title,
            "done": task.done,
        })

    def delete(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**`tasks/urls.py`:**

```python
from django.urls import path
from tasks.views import TaskListView, TaskDetailView

urlpatterns = [
    path("", TaskListView.as_view()),
    path("<int:task_id>/", TaskDetailView.as_view()),
]
```

**`config/urls.py`** (unchanged from Phase E):

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

## To repeat Phase G from scratch

1. Add DRF imports to `tasks/views.py`: `APIView`, `Response`, `status`, `get_object_or_404`
2. Replace `task_list` function with `TaskListView(APIView)` — `get()` and `post()` methods
3. Replace `task_detail` function with `TaskDetailView(APIView)` — `get()`, `put()`, `delete()` methods
4. Remove `import json` and `csrf_exempt` imports entirely
5. Update `tasks/urls.py` — use `TaskListView.as_view()` and `TaskDetailView.as_view()`
6. Test all four HTTP methods with `curl`

---

## Phase G — End state

| What changed from Phase F | Status |
|---|---|
| `task_list` function → `TaskListView(APIView)` | ✅ |
| `task_detail` function → `TaskDetailView(APIView)` | ✅ |
| `@csrf_exempt` removed from all views | ✅ |
| `json.loads(request.body)` replaced with `request.data` | ✅ |
| `if request.method ==` branches replaced with class methods | ✅ |
| `JsonResponse` replaced with `Response` | ✅ |
| Hardcoded status integers replaced with `status.*` constants | ✅ |
| `try/except Task.DoesNotExist` replaced with `get_object_or_404` | ✅ |
| Manual dict building in views | ✅ still present — removed in Phase H |
| Input validation | ❌ Phase J |
| Authentication | ❌ Phase N |
