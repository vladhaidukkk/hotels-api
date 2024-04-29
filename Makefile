lock:
	@pip-compile --upgrade -o requirements.txt
	@pip-compile --extra dev --upgrade -o requirements-dev.txt

sync:
	@pip-sync requirements.txt

sync-dev:
	@pip-sync requirements-dev.txt

run-dev:
	@uvicorn app.main:app --port 8000 --reload

fmt:
	@isort app
	@black app

lint:
	@pyright app
	@flake8 app
	@autoflake -r app
	@bandit -c pyproject.toml -q -r app
