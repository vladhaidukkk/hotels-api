FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /usr/src/app/docker/*.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
