# Phase F — Plain Django JSON Views for Writing Data (Feel the Pain)

## Theory — Why write views are harder than read views

GET views only read data — no validation, no body parsing, no state change. Write views (POST, PUT, DELETE) introduce three new problems:

1. **Request body parsing** — the client sends JSON in the request body. Django does not parse it automatically. You must call `json.loads(request.body)` manually.
2. **CSRF protection** — Django blocks every POST/PUT/DELETE that does not carry a CSRF token. This is correct for browser+session apps but wrong for a JWT API.
3. **Method routing** — Django's URL router matches by path only, not by HTTP method. Two different operations on the same path (GET all vs POST create) must be handled inside a single view function using `if request.method ==` branches.

Phase F adds all four write operations manually so you feel every problem. Phase G (DRF) removes all of them.

---

## What you did

### Step 28 — POST view: parse `request.body` and create a task

**Theory — `request.body` and `json.loads`**

Django does not auto-parse JSON request bodies. The raw bytes arrive in `request.body`. You must decode them with `json.loads()`. If the client sends malformed JSON or omits `Content-Type: application/json`, this raises an exception — there is no built-in error handling at this stage.

**`tasks/views.py`** — merge POST into `task_list`:

```python
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def task_list(request):
    if request.method == "GET":
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

    if request.method == "POST":
        body = json.loads(request.body)
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return JsonResponse(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=201,
        )
```

`tasks/urls.py` does not change — `path("", task_list)` handles both GET and POST on `/tasks/`.

**Why `status=201`:** HTTP 201 Created is the correct response for a successful resource creation. 200 OK is for reads. Using the wrong code is silent — Django does not enforce it.

---

### Step 29 — Theory: CSRF

**What CSRF is:**
CSRF (Cross-Site Request Forgery) is an attack where a malicious website tricks a logged-in user's browser into sending a request to your server. The browser automatically includes the user's session cookie, so the server cannot tell the request is forged.

**How Django blocks it:**
Django's `CsrfViewMiddleware` checks every POST/PUT/DELETE request for a valid `csrftoken`. The token is set in a cookie on the first GET and must be echoed back in a header or form field on every state-changing request. If the token is missing or wrong, Django returns 403 Forbidden before the view function runs.

**Why our `curl` POST gets 403:**
`curl` sends no CSRF token. Django rejects it with an HTML 403 page — not JSON. `python -m json.tool` then fails with `Expecting value` because the body is HTML, not JSON.

**Why we bypass it here:**
CSRF protects session-cookie-based auth. In a JWT API, the React frontend sends a `Bearer` token in the `Authorization` header — no session cookie, nothing for CSRF to protect. `@csrf_exempt` disables the check for a specific view. In Phase G, DRF handles this correctly via its authentication classes and `@csrf_exempt` is removed entirely.

---

### Step 30 — `@csrf_exempt` on write views

Add the import and decorator to every view that handles write methods:

```python
from django.views.decorators.csrf import csrf_exempt
```

Apply `@csrf_exempt` to `task_list` (handles POST) and `task_detail` (handles PUT and DELETE).

**Test POST:**

```bash
# Create a new task
curl -s -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New task"}' | python -m json.tool
```

**Expected response:**

```json
{
    "task_id": 4,
    "title": "New task",
    "done": false
}
```

```bash
# Verify it appears in the list
curl -s http://localhost:8000/tasks/ | python -m json.tool
```

```bash
# Create a task with done=true
curl -s -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Already done", "done": true}' | python -m json.tool
```

---

### Step 31 — PUT view: parse JSON and update a task

**Theory — partial updates with `body.get(field, existing_value)`**

A PUT request may send only the fields the client wants to change. Using `body.get("title", task.title)` keeps the existing value if `title` is absent from the request body. This is partial update behavior. Strict REST defines PUT as a full replacement — but for this learning exercise, partial update is more practical and avoids requiring all fields on every update.

**`tasks/views.py`** — add PUT handling to `task_detail`:

```python
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
```

`task.save()` executes `UPDATE tasks SET title=..., done=... WHERE task_id=...`. Without `save()`, the changes exist only in memory and are never written to Postgres.

**Test PUT:**

```bash
# Update only the done field — title should stay unchanged
curl -s -X PUT http://localhost:8000/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | python -m json.tool
```

**Expected response:**

```json
{
    "task_id": 1,
    "title": "Buy groceries",
    "done": true
}
```

```bash
# Update both fields
curl -s -X PUT http://localhost:8000/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and milk", "done": true}' | python -m json.tool
```

```bash
# Try updating a task that does not exist
curl -s -X PUT http://localhost:8000/tasks/999/ \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | python -m json.tool
```

**Expected response:**

```json
{
    "error": "Task not found"
}
```

---

### Step 32 — DELETE view: remove a task by id

**Theory — HTTP 204 No Content**

204 is the correct status for a successful DELETE. It means "the operation succeeded and there is no response body." Returning 200 with an empty body is technically wrong — 200 implies a body. Django does not enforce this; you must remember it manually.

**`tasks/views.py`** — add DELETE handling to `task_detail`:

```python
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

**Test DELETE:**

```bash
# Delete task 1 — check headers with -i
curl -si -X DELETE http://localhost:8000/tasks/1/
```

**Expected response:**

```
HTTP/1.1 204 No Content
```

```bash
# Verify task 1 is gone
curl -s http://localhost:8000/tasks/ | python -m json.tool
```

```bash
# Try deleting a task that does not exist
curl -si -X DELETE http://localhost:8000/tasks/999/
```

**Expected response:**

```
HTTP/1.1 404 Not Found
{"error": "Task not found"}
```

---

### Step 33 — Theory: Notice the repetition (motivation for DRF)

No files change. Look at what was written manually across Phase F:

| Problem | Manual work done |
|---|---|
| CSRF | `@csrf_exempt` on every write view |
| Request body parsing | `json.loads(request.body)` in every write view |
| HTTP method routing | `if request.method ==` branches in every view |
| Response serialization | Manual dict building in every view |
| Error responses | `try/except Task.DoesNotExist` written by hand |
| Status codes | Hardcoded integers — 201, 204, 404 |

In a real API with 10 resources, this work multiplies by 10. A mistake in one place (wrong status code, missing `@csrf_exempt`, forgetting `safe=False`) is silent — Django does not catch it.

**What DRF replaces:**

| Manual work | DRF replacement |
|---|---|
| `@csrf_exempt` | Handled by authentication classes |
| `json.loads(request.body)` | `request.data` — auto-parsed |
| `if request.method ==` | Class methods: `get()`, `post()`, `put()`, `delete()` |
| Manual dict building | Serializers |
| `try/except Task.DoesNotExist` | `get_object_or_404` or serializer validation |
| Hardcoded integers | `status.HTTP_201_CREATED`, `status.HTTP_204_NO_CONTENT` |

Phase G introduces DRF one layer at a time — `APIView` first, then serializers, then generic views, then viewsets — so you feel what each layer replaces.

---

## Final file state

**`tasks/views.py`:**

```python
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Task


def health(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def task_list(request):
    if request.method == "GET":
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

    if request.method == "POST":
        body = json.loads(request.body)
        task = Task.objects.create(
            title=body["title"],
            done=body.get("done", False),
        )
        return JsonResponse(
            {"task_id": task.task_id, "title": task.title, "done": task.done},
            status=201,
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

**`tasks/urls.py`** (unchanged from Phase E):

```python
from django.urls import path
from tasks.views import task_list, task_detail

urlpatterns = [
    path("", task_list),
    path("<int:task_id>/", task_detail),
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

## To repeat Phase F from scratch

1. Add `import json` and `from django.views.decorators.csrf import csrf_exempt` to `tasks/views.py`
2. Add `@csrf_exempt` to `task_list`, add POST branch inside it
3. Add `@csrf_exempt` to `task_detail`, add PUT and DELETE branches inside it
4. Test POST: `curl -s -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" -d '{"title": "New task"}'`
5. Test PUT: `curl -s -X PUT http://localhost:8000/tasks/1/ -H "Content-Type: application/json" -d '{"done": true}'`
6. Test DELETE: `curl -si -X DELETE http://localhost:8000/tasks/1/`

---

## Phase F — End state

| What exists | Status |
|---|---|
| POST view — create task | ✅ |
| PUT view — update task | ✅ |
| DELETE view — remove task | ✅ |
| CSRF bypassed with `@csrf_exempt` | ✅ |
| All four HTTP verbs working | ✅ |
| DRF views | ❌ Phase G |
| Input validation | ❌ Phase J |
| Authentication | ❌ Phase N |
