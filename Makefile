start-docker:
	docker compose up --force-recreate --build -d

stop-docker:
	docker compose down

start-python:
	sh tools/run.sh

start-python-maintenance:
	sh tooks/run-maintenance.sh
