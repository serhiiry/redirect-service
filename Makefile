DOCKER_IMAGE_NAME=redirect-service
DOCKER_CONTAINER_NAME=redirect-service-container

.PHONY: dev test run

dev:
	pip install poetry
	poetry install

test:
	poetry run pytest

run:
	docker stop $(DOCKER_CONTAINER_NAME) || true
	docker rm $(DOCKER_CONTAINER_NAME) || true
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker run --name $(DOCKER_CONTAINER_NAME) -p 80:80 $(DOCKER_IMAGE_NAME)
