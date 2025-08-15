dev:
	@echo "dev environment"

test:
	pytest -q

up:
	docker compose up --build

build:
	npm --prefix web/app run build
