NAME = $(shell appv name)
IMAGE = $(shell appv image)
VERSION = $(shell appv version)

export MQ_EXCHANGE=x-news
export MQ_SCRAPE_QUEUE=q-scrape-targets
export MQ_SCRAPED_QUEUE=q-scraped-articles
export MQ_HOST=localhost
export MQ_PORT=5672
export MQ_USER=newsscraper
export MQ_PASSWORD=password
export HEARTBEAT_FILE=/tmp/news-scraper-health.txt
export HEARTBEAT_INTERVAL=20

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
