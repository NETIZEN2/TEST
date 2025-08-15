FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir fastapi uvicorn
COPY services/api ./services/api
CMD ["python", "-m", "services.api.main"]
