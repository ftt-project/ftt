test:
	docker-compose run -e ENV_FILE=.env.test trade pytest -s tests