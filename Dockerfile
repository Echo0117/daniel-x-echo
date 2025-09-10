FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy only what you need
COPY main_flask.py .
COPY app ./app
COPY static ./static

EXPOSE 8000
CMD ["gunicorn","-w","1","-k","gthread","--threads","8","-b","0.0.0.0:8000","main_flask:app"]
