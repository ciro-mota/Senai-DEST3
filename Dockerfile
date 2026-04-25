FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "django>=6.0.3,<7.0"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
