dev:
	@echo "dev environment"

test:
	pytest -q

up:
	docker compose up --build
