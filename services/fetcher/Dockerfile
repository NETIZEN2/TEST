FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir requests
COPY services/fetcher ./services/fetcher
CMD ["python", "-m", "services.fetcher.fetcher"]
