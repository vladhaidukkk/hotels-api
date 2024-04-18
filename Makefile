lock:
	@pip-compile --upgrade -o requirements.txt

sync:
	@pip-sync requirements.txt
