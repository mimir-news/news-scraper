# Standard library
import logging

# 3rd party modules
import pika

# Internal modules
from app.config import MQConfig  # Import first to setup logging config.
from app.worker import Worker
from app.service import ScoringService, ScoringService
from app.service import MQConsumer, MQClient


_log = logging.getLogger(__name__)


_config = MQConfig()
mq_conn = pika.BlockingConnection(pika.URLParameters(_config.URI()))
channel = mq_conn.channel()

_scraper = ScoringService()
_scorer = ScoringService()
_mq_client = MQClient(_config, channel)

_worker = Worker(_scraper, _scorer, _mq_client)
app = MQConsumer(_config, channel, _worker)


def teardown_application() -> None:
    channel.close()
    mq_conn.close()
