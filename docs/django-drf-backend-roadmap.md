# Django + DRF Backend Learning Roadmap

> A step-by-step learning roadmap for building a Django + Django REST Framework API backend from nothing to a basic production-grade server. Each step introduces exactly one new concept.

---

## SECTION 1 — Context (read this first)

### Goal

Build a Django + Django REST Framework (DRF) API-only backend in Python, one very small step at a time. Each step introduces exactly one new concept — no leaps, no combining ideas. Learning comes from feeling the gap in each step and then filling it in the next step. The roadmap progresses from an empty folder to a basic production-aware backend.

The learner is in active learning mode and does not want to skip any concepts. Theory-only steps are accepted and encouraged where a new concept must be introduced before an action step uses it.

### Fixed decisions

These are locked. Do not change them mid-roadmap.

1. **Language and framework:** Python 3.10+ with Django and Django REST Framework (DRF). DRF is introduced in layers — plain Django views first, then DRF `APIView`, then serializers, then generic views, then viewsets — so the learner feels what each DRF layer is solving.
2. **Database:** PostgreSQL from the start. The learner already has PostgreSQL running on port 5432 via Docker. No SQLite phase, no local Postgres installation steps. The roadmap only covers connecting Django to the existing Postgres instance.
3. **Resource modeled:** `tasks` — a simple to-do entity with fields `id`, `title`, `done`. Same resource as the companion Express roadmap, so the learner can compare the two frameworks on the same problem.
4. **API-only backend:** No Django templates. No `render()` calls in views. No Django template language. No static UI file serving. No WhiteNoise. No `collectstatic` for frontend assets. The frontend is React and runs separately. Django returns JSON only.
5. **Authentication:** JWT via `djangorestframework-simplejwt`. Not session auth, not token auth — because the React frontend is a separate origin and will use bearer tokens.
6. **Configuration tool:** `python-decouple` for environment variables. Single choice, no alternatives offered.
7. **Setup is interleaved with features.** Setup is not a one-time prerequisite. It grows with the app. Setup steps and feature steps are mixed in the order they become necessary.
8. **HTTP verbs:** All four (GET, POST, PUT, DELETE) must be covered at appropriate points in the roadmap.

### Prerequisites the learner already has

The roadmap does not teach these. They are assumed:

- A Docker-based Python development environment is already running. No venv setup steps are needed.
- Docker installed and a PostgreSQL container running on port 5432, accessible from the host.
- Basic Python knowledge (functions, classes, imports, decorators).
- Basic command-line knowledge.

### Step format

Every step has exactly these three parts, in this order:

1. **What we add in this step** — the one small change. For theory-only steps, this says "this is a theory step, no files change" and names the concept being introduced.
2. **What problem existed in the previous step** — the motivation. For Step 1, this is "nothing exists yet."
3. **How this step solves that problem** — the explanation.

Each part is 2–3 sentences maximum.

**Mermaid diagrams and Theory sections are not included in this file.** Ask for them in chat when needed for a specific step.

### Two kinds of steps in this roadmap

- **Action steps** — change files, install packages, run commands. The majority of steps.
- **Theory-only steps** — introduce a new concept before an action step uses it. No files change. Django has more conceptual surface area than Express, so theory-only steps are necessary to avoid hidden leaps.

### Full step list (table of contents) — 94 walkthrough steps + 1 reference step

**Phase A — Python project and Django bootstrap**

1. Install Django and Django REST Framework
2. Freeze dependencies into `requirements.txt`
3. Create the Django project with `django-admin startproject`
4. **[theory]** Understand the project layout `startproject` created
5. Create a Django app for tasks with `python manage.py startapp`
6. **[theory]** Understand the app layout `startapp` created and the project-vs-app distinction
7. **[theory]** Understand what `INSTALLED_APPS` is and why Django needs apps to be registered
8. Register the tasks app in `INSTALLED_APPS`
9. Register `rest_framework` in `INSTALLED_APPS`

**Phase B — Connect Django to PostgreSQL** 10. Create a dedicated database and user inside the running Postgres 11. Install the `psycopg` driver 12. Configure the `DATABASES` setting to point at Postgres 13. Run initial `migrate` to create Django's built-in tables in Postgres

**Phase C — First HTTP response (no database, no model)** 14. **[theory]** Understand how Django handles a request — URL resolver, view function, response object 15. Add a function-based view that returns a hardcoded JSON response 16. Wire the view into the project's root `urls.py` 17. Start the dev server with `runserver` and hit the endpoint

**Phase D — The Task model and first real data** 18. **[theory]** Understand what a Django model is and how it maps to a database table 19. Define the `Task` model with `id`, `title`, `done` fields 20. Run `makemigrations` to generate the migration file 21. Run `migrate` to apply the migration and create the `tasks` table 22. Open the Django shell and create a few tasks manually to verify the model works

**Phase E — Plain Django JSON views for reading data** 23. **[theory]** Introduce `Task.objects.all()` and explain what a QuerySet is 24. Replace the hardcoded view with one that queries all tasks and builds a JSON response manually 25. Add a detail view that returns a single task by id 26. Handle the "task not found" case manually with a 404 JSON response 27. Split tasks URLs into the app's own `urls.py` and include it from the project `urls.py`

**Phase F — Plain Django JSON views for writing data (feel the pain)** 28. Add a POST view that parses JSON from `request.body` manually and creates a task 29. **[theory]** Understand what CSRF is, why Django enforces it, and why we will temporarily bypass it 30. Exempt the POST view from CSRF with `@csrf_exempt` 31. Add a PUT view that parses JSON and updates a task manually 32. Add a DELETE view that removes a task by id 33. Notice the repetition and manual work across all four write views — motivation for DRF

**Phase G — Introduce DRF one layer at a time** 34. **[theory]** Understand class-based views and why DRF uses them 35. Convert the list view to a DRF `APIView` using `Response` and `status` 36. Convert the detail view to an `APIView` and use `get_object_or_404` 37. Convert POST, PUT, DELETE views into `post`, `put`, `delete` methods on a single `APIView` class 38. Remove `@csrf_exempt` — DRF handles CSRF differently via authentication classes

**Phase H — DRF serializers** 39. Create a `TaskSerializer` using `serializers.ModelSerializer` 40. Use the serializer to replace manual dict building in the list and detail views 41. Use the serializer to validate incoming data in the POST view 42. Use the serializer for PUT by passing the existing instance plus new data

**Phase I — DRF generic views and viewsets** 43. **[theory]** Understand DRF generic views and the mixin pattern 44. Replace the list and create `APIView` with `ListCreateAPIView` 45. Replace the detail/update/delete `APIView` with `RetrieveUpdateDestroyAPIView` 46. **[theory]** Understand what a DRF viewset is and how it differs from a generic view 47. Collapse both generic views into a single `ModelViewSet` 48. Wire the viewset into URLs using DRF's `DefaultRouter`

**Phase J — Input validation refinement** 49. Add field-level validation on the serializer (title minimum length, cannot be blank) 50. Add object-level validation using the serializer's `validate` method 51. Strip whitespace from the `title` field on input 52. **[theory]** Understand DRF's default exception handler and what errors currently look like 53. Customize the DRF exception handler to return a consistent error shape

**Phase K — Configuration and secrets** 54. Install `python-decouple` 55. Move `SECRET_KEY` into an environment variable 56. Move `DEBUG` into an environment variable 57. Move `DATABASES` credentials into environment variables 58. Configure `ALLOWED_HOSTS` from an environment variable

**Phase L — CORS (React frontend needs this)** 59. Install `django-cors-headers` 60. Add the CORS middleware and configure allowed origins for the React dev server

**Phase M — Logging** 61. Configure Django's `LOGGING` setting with a basic formatter and console handler 62. Add a middleware that generates a unique request id and attaches it to the request 63. Include the request id in every log line for that request 64. Add a middleware that logs every request (method, path, status, duration)

**Phase N — Authentication and authorization** 65. **[theory]** Understand what JWT is and how stateless token auth differs from session auth 66. Install `djangorestframework-simplejwt` 67. Configure JWT as the default DRF authentication class 68. Add the JWT obtain and refresh endpoints to URLs 69. **[theory]** Understand the distinction between authentication and permissions in DRF 70. Add `DEFAULT_PERMISSION_CLASSES` requiring authentication by default 71. **[theory]** Understand `has_permission` vs `has_object_permission` and when each is called 72. Add a permission class that only allows task owners to modify their own tasks 73. Add a nullable `user` foreign key to the `Task` model and migrate 74. Delete existing tasks and make the `user` field non-nullable, then migrate again 75. Update the viewset to set the owner automatically on create and filter the queryset by owner on list

**Phase O — Rate limiting and security headers** 76. Configure DRF throttling (anonymous and authenticated rate limits) 77. Set Django's security-related settings (`SECURE_*` flags) appropriately for API-only

**Phase P — Production behavior** 78. Add a liveness health check endpoint 79. Add a readiness health check endpoint (checks database reachability) 80. Replace `runserver` with Gunicorn for production serving 81. Configure graceful shutdown handling in Gunicorn's worker configuration

**Phase Q — API versioning and error shape** 82. Add URL-based API versioning with a `/v1/` prefix 83. Configure DRF's `URLPathVersioning` class 84. Finalize a consistent error response shape across all DRF error paths

**Phase R — Testing** 85. Run `manage.py test` with no tests written and observe the test database lifecycle 86. Write a unit test for the serializer's validation 87. Write an integration test for the list endpoint using DRF's `APITestCase` 88. Write integration tests for create, update, and delete endpoints 89. Write a test that verifies JWT authentication is enforced on protected endpoints

**Phase S — API documentation** 90. Install `drf-spectacular` 91. Configure `drf-spectacular` as the DRF schema class 92. Add URL routes for the OpenAPI schema and Swagger UI

**Phase T — Shipping** 93. Create a `Dockerfile` for the Django app (Gunicorn-based) 94. Add a `.dockerignore` file

**Phase U — Future reference only (not walked through)** 95. Reference list of topics to learn after this roadmap is complete: Celery for background jobs, Redis caching (via `django-redis`), Django signals, custom management commands, Django Channels for WebSockets, database query optimization (`select_related`, `prefetch_related`, Django Debug Toolbar), database indexing strategies, metrics (`django-prometheus`), distributed tracing (OpenTelemetry), circuit breakers for external calls, retries with exponential backoff, idempotency keys for safe write retries, multi-database routing, read replicas, and PostgreSQL-specific features (full-text search, JSONB fields, partial indexes).

### Current status

**Last completed step: 33** (completed Phase F)

**Next step to write: 34** (start of Phase G)

---

## SECTION 2 — Detailed steps

### Step 1 — Install Django and Django REST Framework

**What we add in this step**
Run `pip install django djangorestframework` inside the container. This downloads Django and DRF from PyPI and installs them into the environment.

**What problem existed in the previous step**
Nothing exists yet — the container has Python but no web framework. Without Django installed, there is no `django-admin` command and no way to create a project.

**How this step solves that problem**
After this command, `import django` and `import rest_framework` both work, and the `django-admin` CLI tool is available for the next step.

---

### Step 2 — Freeze dependencies into `requirements.txt`

**What we add in this step**
Run `pip freeze > requirements.txt` to capture every installed package and its exact version into a file at the project root.

**What problem existed in the previous step**
Django and DRF are installed but there is no record of which versions. Rebuilding the container later would pull whatever the latest versions are at that moment, which may differ from what was tested.

**How this step solves that problem**
`requirements.txt` acts as a reproducible manifest — anyone (or any CI system) can run `pip install -r requirements.txt` and get the exact same environment. Re-run `pip freeze` every time a new package is installed to keep the file in sync.

---

### Step 3 — Create the Django project with `django-admin startproject`

**What we add in this step**
Run `django-admin startproject config .` inside the project folder. The trailing dot places `manage.py` and the `config/` package in the current directory instead of creating an extra nested folder.

**What problem existed in the previous step**
Django is installed but there is no project structure yet — no `settings.py`, no URL routing entry point, no `manage.py`. Without these, nothing can run.

**How this step solves that problem**
`startproject` scaffolds the minimum files Django needs to start: `manage.py` for running commands, `config/settings.py` for configuration, `config/urls.py` for routing, and `config/wsgi.py` / `config/asgi.py` for production deployment interfaces.

---

### Step 4 — Understand the project layout `startproject` created (theory only)

**What we add in this step**
This is a theory step, no files change. The concept introduced is the purpose of each file that `startproject` generated.

**What problem existed in the previous step**
The project folder now contains several unfamiliar files. Editing the wrong one or misunderstanding the separation between configuration files and application code is the most common Django beginner mistake.

**How this step solves that problem**
`manage.py` is the command-line entry point for all Django commands. `settings.py` is the central configuration module — all future configuration steps edit this file. `urls.py` is the top-level routing entry point. `wsgi.py` and `asgi.py` are the production server interfaces that you rarely touch directly.

---

### Step 5 — Create a Django app for tasks with `python manage.py startapp`

**What we add in this step**
Run `python manage.py startapp tasks`. This creates a `tasks/` folder in the project root containing `models.py`, `views.py`, `admin.py`, `apps.py`, `tests.py`, and a `migrations/` subfolder.

**What problem existed in the previous step**
The project exists but has no place to put application code. Putting task models and views directly inside `config/` would mix configuration with feature code, which Django's architecture is designed to prevent.

**How this step solves that problem**
The `tasks/` app is now the bounded container for all task-related code — the `Task` model goes in `models.py`, task views go in `views.py`, and migrations go in `migrations/`. Future steps will fill these files.

---

### Step 6 — Understand the app layout `startapp` created and the project-vs-app distinction (theory only)

**What we add in this step**
This is a theory step, no files change. The concept introduced is the purpose of each file in the `tasks/` app and the distinction between a Django project and a Django app.

**What problem existed in the previous step**
The `tasks/` folder has several generated files whose roles are not yet clear. Without understanding the project-vs-app split, it is not obvious where new code should go.

**How this step solves that problem**
A Django _project_ is the overall deployable unit (one settings file, one URL entry point). A Django _app_ is a self-contained feature module within that project. `models.py` holds database models, `views.py` holds request handlers, `migrations/` holds schema change files, and `tests.py` holds tests for this app.

---

### Step 7 — Understand what `INSTALLED_APPS` is and why Django needs apps to be registered (theory only)

**What we add in this step**
This is a theory step, no files change. The concept introduced is `INSTALLED_APPS` in `settings.py` and why Django requires explicit app registration.

**What problem existed in the previous step**
The `tasks` app exists on disk but Django does not know it exists. If you ran `makemigrations` now, Django would silently skip the `tasks` app and report "no changes detected" — a confusing failure with no error message.

**How this step solves that problem**
`INSTALLED_APPS` is a list of strings in `settings.py` that tells Django which apps are active. On startup, Django only loads models, migrations, and templates from apps listed here. Registering an app is the explicit declaration that connects the app's code to Django's runtime.

---

### Step 8 — Register the tasks app in `INSTALLED_APPS`

**What we add in this step**
Open `config/settings.py`, find the `INSTALLED_APPS` list, and add `"tasks"` as a new entry.

**What problem existed in the previous step**
The `tasks` app is not registered, so Django ignores it entirely. Any model defined in `tasks/models.py` would be invisible to migrations and the ORM.

**How this step solves that problem**
Adding `"tasks"` tells Django to import the app at startup, register its models, and include its `migrations/` folder in the migration graph. The next time any Django command runs, the `tasks` app is a first-class part of the project.

---

### Step 9 — Register `rest_framework` in `INSTALLED_APPS`

**What we add in this step**
Open `config/settings.py` again and add `"rest_framework"` to `INSTALLED_APPS`, placed after Django's built-in apps and before `"tasks"`.

**What problem existed in the previous step**
DRF is installed as a Python package (Step 1) but Django does not know it is in use. Without registration, DRF's default settings are not loaded and its browsable API templates are not found.

**How this step solves that problem**
Registering `"rest_framework"` activates DRF's integration with Django's startup: the `REST_FRAMEWORK` settings dict becomes active, DRF's template loaders work, and its management commands are available. Phase A ends here — the project is bootstrapped and both apps are registered.

---

## SECTION 3 — Resume instructions (for the next Claude in the next chat)

**If you are a Claude instance reading this file in a new chat, read this section carefully.**

### What this file is

This is a learning roadmap being built incrementally across multiple chat sessions. The user is learning Django + Django REST Framework by working through small steps. The file is the handoff document between chat sessions — it carries all the context needed to continue the work without the user having to re-explain anything.

### What you must do

1. **Read Section 1 completely.** It contains the goal, the fixed decisions (locked — do not change them), the prerequisites, the step format specification, and the full 94-step list plus 1 reference step.

2. **Read Section 2 completely.** Match the established writing style exactly — three parts per step, 2–3 sentences each, no diagrams, no theory blocks in the file.

3. **Check the "Current status" line in Section 1.** It says "Last completed step: X". The next step to write is X+1.

4. **Write the next chunk of steps** in the same three-part format, appending to Section 2 in order. A reasonable chunk is one full phase, or 5–8 steps, whichever is smaller.

5. **Update the "Current status" line** in Section 1 to reflect the new last-completed step and the new next step.

6. **Return the updated file to the user** using the file creation tool.

### Format rules you must follow

- **Three parts per step, in this order:** (1) What we add, (2) What problem existed in the previous step, (3) How this step solves that problem.
- **2–3 sentences per part maximum.** No long paragraphs.
- **No Mermaid diagrams in the file.** Provide them in chat only when the user asks.
- **No Theory sections in the file.** Provide theory in chat only when the user asks.
- **Theory-only steps still follow the three-part format.** Part 1 says "This is a theory step, no files change" and names the concept.
- **No code blocks.** Inline references to file names, class names, method names are fine. No multi-line code or folder trees.
- **Python + Django + DRF only.** No comparisons to other frameworks unless the user asks.
- **Each step is one small change.** If a step feels like two changes, flag it instead of merging.
- **Match the tone:** technical, direct, no filler, no motivational language, no emojis. Clear and precise wording — the user's first language is not English.

### What not to do

- Do not rewrite Section 1. It is locked.
- Do not rewrite previously completed steps in Section 2. They are locked.
- Do not skip steps or reorder them.
- Do not add new steps not in the list without asking the user first.
- Do not change the fixed decisions.
- Do not suggest SQLite as a development alternative.
- Do not ask clarifying questions already answered in Section 1.

### How the user will prompt you

The user will say something short like "continue the roadmap" or "write next phase". The file is the full context — no additional information is needed.

### When the roadmap is complete

When Step 94 is written, update "Current status" to "Roadmap complete. All 94 walkthrough steps written." Add a short note reminding the user that Phase U (step 95) is listed in Section 1 as future reference and is intentionally not walked through.

### Companion roadmap

The user has a parallel Express.js roadmap using the same format and `tasks` resource. If both files are uploaded in the same chat, treat them as independent — do not cross-reference or sync them.
