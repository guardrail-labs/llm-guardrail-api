.PHONY: demo up down smoke

demo: up smoke

up:
	docker compose -f examples/docker-compose.yml up -d

down:
	docker compose -f examples/docker-compose.yml down -v

smoke:
	bash examples/smoke.sh
