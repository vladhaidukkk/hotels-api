default: fmt lint

# Dependencies Management
lock:
    pip-compile --upgrade -o requirements.txt
    pip-compile --extra dev --upgrade -o requirements-dev.txt

sync:
    pip-sync requirements.txt

sync-dev:
    pip-sync requirements-dev.txt

# Code Formatting & Linting
fmt:
    isort app
    black app
    docformatter app

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

# Database Management
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
