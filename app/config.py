# Standard library
import os
import logging
from logging.config import dictConfig


NUM_WORKERS: int = 5


class MQConfig:
    EXCHANGE: str = os.environ['MQ_EXCHANGE']
    SCRAPE_QUEUE: str = os.environ['MQ_SCRAPE_QUEUE']
    SCRAPED_QUEUE: str = os.environ['MQ_SCRAPED_QUEUE']
    _host: str = os.environ['MQ_HOST']
    _port: str = os.environ['MQ_PORT']
    _user: str = os.environ['MQ_USER']
    _password: str = os.environ['MQ_PASSWORD']

    def URI(self) -> str:
        return f'amqp://{self._user}:{self._password}@{self._host}:{self._port}/'


class HeartbeetConfig:
    FILE: int = int(os.environ['HEARTBEAT_FILE'])
    INTERVAL: int = os.environ['HEARTBEAT_INTERVAL']


LOGGING_CONIFG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.INFO
        }
    },
    'root': {
        'handlers': ['console'],
        'level': logging.DEBUG
    }
}

dictConfig(LOGGING_CONIFG)
