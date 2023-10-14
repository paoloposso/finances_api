db-start:
	docker-compose up -d

db-stop:
	docker-compose down

test:
	pipenv run pytest
