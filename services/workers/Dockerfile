FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir celery redis
COPY services/workers ./services/workers
CMD ["python", "-m", "services.workers.tasks"]
