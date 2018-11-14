# Standard library
import logging

# 3rd party modules
import pika

# Internal modules
from app.config import MQConfig  # Import first to setup logging config.
from app.worker import Worker
from app.service import ScrapingService, ScoringService
from app.service import MQConsumer, MQClient, MQConnectionFactory


_log = logging.getLogger(__name__)


_config = MQConfig()
_factory = MQConnectionFactory(_config)
channel = _factory.get_channel()

_scraper = ScrapingService()
_scorer = ScoringService()
_mq_client = MQClient(_config, channel)

_worker = Worker(_scraper, _scorer, _mq_client)
app = MQConsumer(_config, channel, _worker)
