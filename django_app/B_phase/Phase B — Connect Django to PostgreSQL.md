# Phase B — Connect Django to PostgreSQL

## What you did

### 1. Docker Compose — database setup
Added `django-lab-db` service to `docker-compose.yml`:

```yaml
django-lab-db:
  image: postgres:18-bookworm
  container_name: django-learning-postgres
  networks:
    - django-network
  environment:
    POSTGRES_DB: django_lab
    POSTGRES_USER: lab_user
    POSTGRES_PASSWORD: lab_pass
  healthcheck:
    test: [ "CMD-SHELL", "pg_isready -U lab_user -d django_lab" ]
    interval: 5s
    timeout: 3s
    retries: 5
```

Database `django_lab` and user `lab_user` are created automatically on first container start.

---

### 2. Install psycopg driver
```bash
uv add "psycopg[binary,pool]"
```

---

### 3. Configure DATABASES in `config/settings.py`

Replace the default SQLite `DATABASES` block:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_lab",
        "USER": "lab_user",
        "PASSWORD": "lab_pass",
        "HOST": "django-learning-postgres",
        "PORT": "5432",
    }
}
```

`HOST` is the Docker service container name, not `localhost`.

---

### 4. Verify config
```bash
uv run python manage.py check --database default
# Expected: System check identified no issues (0 silenced).
```

---

### 5. Apply migrations
```bash
uv run python manage.py migrate
# Expected: list of "Applying ...OK" lines, no errors
```

**Result:** 10 built-in tables created in `django_lab`:

| Table | App |
|---|---|
| `django_migrations` | core |
| `django_content_types` | contenttypes |
| `auth_permission` | auth |
| `auth_group` | auth |
| `auth_group_permissions` | auth |
| `auth_user` | auth |
| `auth_user_groups` | auth |
| `auth_user_user_permissions` | auth |
| `django_admin_log` | admin |
| `django_session` | sessions |

---

## To repeat Phase B from scratch

1. Start containers: `docker compose up -d`
2. `uv add "psycopg[binary,pool]"`
3. Edit `config/settings.py` — replace `DATABASES` as above
4. `uv run python manage.py check --database default`
5. `uv run python manage.py migrate`

---

## Phase B — End state

| What exists | Status |
|---|---|
| Postgres container running | ✅ |
| psycopg driver installed | ✅ |
| Django connected to Postgres | ✅ |
| Built-in tables created | ✅ |
| Task model | ❌ Phase D |
| Any URL or view | ❌ Phase C |
