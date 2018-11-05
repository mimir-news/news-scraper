NAME = $(shell appv name)
IMAGE = $(shell appv image)
VERSION = $(shell appv version)

run:
	python main.py

test:
	mypy --ignore-missing-imports main.py

install:
	pip install -r requirements.txt

build:
	docker build -t $(IMAGE) .

build-test:
	docker build -t "$(NAME)-test:$(VERSION)" -f Dockerfile.test .
