# Phase D — The Task Model and First Real Data

## What you did

### 1. Define the `Task` model in `tasks/models.py`

```python
from django.db import models


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return self.title
```

`db_table = "tasks"` overrides Django's default table name of `tasks_task`.  
`task_id` is an explicit `AutoField` primary key — equivalent to `SERIAL PRIMARY KEY` in Postgres.

---

### 2. Generate the migration file

```bash
uv run python manage.py makemigrations tasks
```

**Expected output:**
```
Migrations for 'tasks':
  tasks/migrations/0001_initial.py
    - Create model Task
```

This generates `tasks/migrations/0001_initial.py`. It describes the schema change in Python — it has not touched Postgres yet.

---

### 3. Apply the migration

```bash
uv run python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, tasks
Running migrations:
  Applying tasks.0001_initial... OK
```

Django executes the equivalent of this SQL against `django_lab`:

```sql
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
```

---

### 4. Verify the table exists

```bash
docker exec -it django-learning-postgres psql -U lab_user -d django_lab -c "\dt"
```

`tasks` should appear in the table list alongside the 10 built-in tables from Phase B.

---

### 5. Open the Django shell and create tasks manually

```bash
uv run python manage.py shell
```

```python
from tasks.models import Task

# Create three tasks
t1 = Task.objects.create(title="Buy groceries")
t2 = Task.objects.create(title="Write tests")
t3 = Task.objects.create(title="Deploy to staging", done=True)

# Read all tasks
Task.objects.all()
# <QuerySet [<Task: Buy groceries>, <Task: Write tests>, <Task: Deploy to staging>]>

# Read single task by primary key
Task.objects.get(task_id=1)
# <Task: Buy groceries>

# Filter by field
Task.objects.filter(done=True)
# <QuerySet [<Task: Deploy to staging>]>

# Verify field values
t = Task.objects.get(task_id=1)
t.task_id   # 1
t.title     # 'Buy groceries'
t.done      # False

exit()
```

---

## To repeat Phase D from scratch

1. Edit `tasks/models.py` — add the `Task` class as above
2. `uv run python manage.py makemigrations tasks`
3. `uv run python manage.py migrate`
4. Verify: `docker exec -it django-learning-postgres psql -U lab_user -d django_lab -c "\dt"`
5. `uv run python manage.py shell` — create and query tasks manually

---

## Phase D — End state

| What exists | Status |
|---|---|
| `Task` model defined | ✅ |
| Migration file generated | ✅ |
| `tasks` table created in Postgres | ✅ |
| Tasks created and queried via shell | ✅ |
| Task URLs and views | ❌ Phase E |
| API responses for tasks | ❌ Phase E |
