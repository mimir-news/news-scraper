# Standard library
import json
import logging
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor

# 3rd party modules
import pika
from pika.channel import Channel
from pika.spec import Basic as MQ
from pika.amqp_object import Properties as MQProperties

# Internal modules
from app.config import MQConfig, NUM_WORKERS
from app.models import ScrapedArticle, ScrapeTarget


class MessageHandler(metaclass=ABCMeta):

    @abstractmethod
    def handle_scrape_target(self,
                             target: ScrapeTarget,
                             channel: Channel,
                             mq_method: MQ.Deliver) -> None:
        pass


class MQClient:

    _log = logging.getLogger('MQClient')

    def __init__(self, config: MQConfig, channel: Channel) -> None:
        self.CONFIG = config
        self._channel = channel

    def send(self, scraped_article: ScrapedArticle) -> None:
        self._channel.basic_publish(
            exchange=self.CONFIG.EXCHANGE,
            routing_key=self.CONFIG.SCRAPED_QUEUE,
            body=json.dumps(scraped_article.asdict(), indent=4, sort_keys=True)
        )

    def ack(self, channel: Channel, method: MQ.Deliver) -> None:
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def reject(self, channel: Channel, method: MQ.Deliver) -> None:
        channel.basic_reject(
            delivery_tag=method.delivery_tag,
            requeue=False)


class MQConsumer:

    _log = logging.getLogger('MQConsumer')

    def __init__(self,
                 config: MQConfig,
                 channel: Channel,
                 handler: MessageHandler) -> None:
        self.CONFIG = config
        self._channel = channel
        self._handler = handler
        self._executor = ThreadPoolExecutor(max_workers=NUM_WORKERS)

    def start(self) -> None:
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            self._handle_message,
            self.CONFIG.SCRAPE_QUEUE)
        self._channel.start_consuming()

    def _handle_message(self,
                        channel: Channel,
                        method: MQ.Deliver,
                        properties: MQProperties,
                        body: bytes) -> None:
        try:
            scrape_target = ScrapeTarget.fromdict(json.loads(body))
            self._log.info(
                f'Handling ScrapeTarget with url={scrape_target.url} '
                f'article_id={scrape_target.article_id}')
            self._handler.handle_scrape_target(scrape_target, channel, method)
        except ValueError as e:
            self._log.info(str(e))
            self._reject_message(method)

    def _reject_message(self, method: MQ.Deliver) -> None:
        self._channel.basic_reject(delivery_tag=method.delivery_tag)
