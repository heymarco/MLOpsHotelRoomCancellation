FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]