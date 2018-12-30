NAME = $(shell appv name)
IMAGE = $(shell appv image)
VERSION = $(shell appv version)

export MQ_EXCHANGE=x-news
export MQ_SCRAPE_QUEUE=q-scrape-targets
export MQ_SCRAPED_QUEUE=q-scraped-articles
export MQ_HEALTH_TARGET=q-health-newsscraper
export MQ_HOST=localhost
export MQ_PORT=5672
export MQ_USER=newsscraper
export MQ_PASSWORD=password
export HEARTBEAT_FILE=/tmp/news-scraper-health.txt
export HEARTBEAT_INTERVAL=20

run:
	python main.py

test:
	sh run-tests.sh

install:
	pip install -r requirements.txt

install-test:
	pip install -r test-requirements.txt

build:
	docker build -t $(IMAGE) .

build-test:
	docker build -t "$(NAME)-test:$(VERSION)" -f Dockerfile.test .

run-container:
	docker run -d --name $(NAME) --network=mimir-net \
		-e MQ_EXCHANGE=$(MQ_EXCHANGE) \
		-e MQ_SCRAPE_QUEUE=$(MQ_SCRAPE_QUEUE) \
		-e MQ_SCRAPED_QUEUE=$(MQ_SCRAPED_QUEUE) \
		-e MQ_HEALTH_TARGET=$(MQ_HEALTH_TARGET) \
		-e MQ_HOST=mq -e MQ_PORT=$(MQ_PORT) \
		-e MQ_USER=$(MQ_USER) -e MQ_PASSWORD=$(MQ_PASSWORD) \
		-e HEARTBEAT_FILE=$(HEARTBEAT_FILE) \
		-e HEARTBEAT_INTERVAL=$(HEARTBEAT_INTERVAL) \
		$(IMAGE)
