FROM python:3.9-slim

RUN mkdir /hotello

WORKDIR /hotello

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /hotello/docker/*.sh

CMD pwd

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", \
"uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
