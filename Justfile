default: fmt lint

# Dependencies Management
lock:
    uv pip compile pyproject.toml -o requirements.txt
    uv pip compile pyproject.toml --extra dev -o requirements-dev.txt

lock-up:
    uv pip compile pyproject.toml --upgrade -o requirements.txt
    uv pip compile pyproject.toml --extra dev --upgrade -o requirements-dev.txt

sync:
    uv pip sync requirements.txt

sync-dev:
    uv pip sync requirements-dev.txt

# Code Formatting & Linting
fmt:
    -isort app
    -black app
    -docformatter app

lint:
    -pyright app
    -flake8 app
    -autoflake app
    -bandit -c pyproject.toml -q -r app

# Run Scripts
run script:
    PYTHONPATH=. python {{script}}

# Serve Application
serve-dev:
    uvicorn app.main:app --port 8000 --reload

# Start Background Tasks (Celery)
start-celery:
    celery -A app.tasks.celery_app:celery_app worker --loglevel=INFO

start-flower:
    celery -A app.tasks.celery_app:celery_app flower

# Database Management
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
