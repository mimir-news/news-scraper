# Standard library
import json
import logging
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor

# 3rd party modules
import pika

# Internal modules
from app.config import MQConfig, NUM_WORKERS
from app.models import ScrapedArticle, ScrapeTarget

# Types
MQChannel = pika.adapters.blocking_connection.BlockingChannel
MQConnection = pika.BlockingConnection
MQDeliver = pika.spec.Basic.Deliver
MQProperties = pika.amqp_object.Properties


class MessageHandler(metaclass=ABCMeta):

    @abstractmethod
    def handle_scrape_target(self, target: ScrapeTarget, mq_method: MQDeliver) -> None:
        pass


class MQClient:

    _log = logging.getLogger('MQClient')

    def __init__(self,
                 config: MQConfig,
                 send_channel: MQChannel,
                 ack_channel: MQChannel) -> None:
        self.CONFIG = config
        self._send_chan = send_channel
        self._ack_chan = ack_channel

    def send(self, scraped_article: ScrapedArticle) -> None:
        self._send_chan.basic_publish(
            exchange=self.CONFIG.EXCHANGE,
            routing_key=self.CONFIG.SCRAPED_QUEUE,
            body=json.dumps(scraped_article.asdict())
        )

    def ack(self, method: MQDeliver) -> None:
        self._ack_chan.basic_ack(delivery_tag=method.delivery_tag)

    def reject(self, method: MQDeliver) -> None:
        self._ack_chan.basic_reject(delivery_tag=method.delivery_tag)


class MQConsumer:

    _log = logging.getLogger('MQConsumer')

    def __init__(self,
                 config: MQConfig,
                 channel: MQChannel,
                 handler: MessageHandler) -> None:
        self.CONFIG = config
        self._channel = channel
        self._handler = handler
        self._executor = ThreadPoolExecutor(max_workers=NUM_WORKERS)

    def start(self) -> None:
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume()
        self._channel.start_consuming()

    def _handle_message(self,
                        channel: MQChannel,
                        method: MQDeliver,
                        properties: MQProperties,
                        body: bytes) -> None:
        try:
            scrape_target = ScrapeTarget.fromdict(json.loads(body))
            self._handler.handle_scrape_target(scrape_target, method)
        except ValueError as e:
            self._log.info(str(e))
            self._reject_message(method)

    def _reject_message(self, method: MQDeliver) -> None:
        self._channel.basic_reject(delivery_tag=method.delivery_tag)
