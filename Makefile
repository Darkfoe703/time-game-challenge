# Makefile
.PHONY: run build up down test logs

build:
	docker-compose build --no-cache

up:
	docker-compose up

down:
	docker-compose down

run:
	docker-compose up --build

test:
	PYTHONPATH=./ pytest -s

logs:
	docker-compose logs -f --tail=100
