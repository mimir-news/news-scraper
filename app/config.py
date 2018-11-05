# Standard library
import os


NUM_WORKERS: int = 5


class MQConfig:
    HOST: str = os.environ['MQ_HOST']
    PORT: str = os.environ['MQ_PORT']
    USER: str = os.environ['MQ_USER']
    PASSWORD: str = os.environ['MQ_PASSWORD']
    EXCHANGE: str = os.environ['MQ_EXCHANGE']
    SCRAPE_QUEUE: str = os.environ['MQ_SCRAPE_QUEUE']
    SCRAPED_QUEUE: str = os.environ['MQ_SCRAPED_QUEUE']


class HeartbeetConfig:
    FILE: int = int(os.environ['HEARTBEAT_FILE'])
    INTERVAL: int = os.environ['HEARTBEAT_INTERVAL']
