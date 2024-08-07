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
    -isort app tests
    -black app tests
    -docformatter app tests

lint:
    -pyright app tests
    -flake8 app tests
    -autoflake app tests
    -bandit -c pyproject.toml -q -r app

# Run Scripts
run script:
    PYTHONPATH=. python {{script}}

# Serve Application
serve-dev:
    uvicorn app.main:app --port 8000 --reload

# Start Background Tasks (Celery)
start-worker:
    NULL_POOL=1 celery -A app.tasks.worker:worker worker --loglevel=INFO

start-beat:
    celery -A app.tasks.worker:worker beat --loglevel=INFO

start-flower:
    celery -A app.tasks.worker:worker flower

# Database Management
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}

# Docker Commands
build-img:
    docker build -t hotels-api .

run-ctr:
    docker run -d -p 8000:8000 hotels-api

build-compose:
    docker compose build

run-compose:
    docker compose up
