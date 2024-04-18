lock:
	@pip-compile --upgrade -o requirements.txt

sync:
	@pip-sync requirements.txt

run-dev:
	@uvicorn app.main:app --port 8000 --reload
