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
	@black app

lint:
	@flake8 app
