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
        """Handles scraping and ranking of an incomming scrape target.

        :param target: ScrapeTarget to handle.
        :param channel: MQ channel to ack or reject the message.
        :param mq_method: MQ metadata about the message.
        """


class MQClient:

    _log = logging.getLogger("MQClient")

    def __init__(self, config: MQConfig, channel: Channel) -> None:
        self.CONFIG = config
        self._channel = channel

    def send(self, scraped_article: ScrapedArticle) -> None:
        self._channel.basic_publish(
            exchange=self.CONFIG.EXCHANGE,
            routing_key=self.CONFIG.SCRAPED_QUEUE,
            body=json.dumps(scraped_article.asdict())
        )

    def ack(self, channel: Channel, method: MQ.Deliver) -> None:
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def reject(self, channel: Channel, method: MQ.Deliver) -> None:
        channel.basic_reject(
            delivery_tag=method.delivery_tag,
            requeue=False)


class MQConsumer:

    _log = logging.getLogger("MQConsumer")

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
                f"Incomming ScrapeTarget articleId=[{scrape_target.article_id}]")
            self._executor.submit(
                self._handler.handle_scrape_target,
                scrape_target, channel, method)
        except ValueError as e:
            self._log.info(str(e))
            self._reject_message(method)

    def _reject_message(self, method: MQ.Deliver) -> None:
        self._channel.basic_reject(delivery_tag=method.delivery_tag)


class MQConnectionChecker(metaclass=ABCMeta):

    def is_connected(self, health_target: str) -> bool:
        """Returns a boolean inidcating if the underlying MQ connenction is open.

        :param health_target: MQ target to use for health checking.
        :return: Boolean
        """
        raise NotImplementedError()


class MQConnectionFactory(MQConnectionChecker):

    _log = logging.getLogger("MQConnectionFactory")

    def __init__(self, config: MQConfig) -> None:
        self.TEST_MODE = config.TEST_MODE
        if not self.TEST_MODE:
            connection_params = pika.URLParameters(config.URI())
            self._conn = pika.BlockingConnection(connection_params)
            self._channel = self._conn.channel()
            self._channel.basic_qos(prefetch_count=NUM_WORKERS)
        else:
            self._conn = None
            self._channel = None

    def __del__(self) -> None:
        if not self.TEST_MODE:
            self._channel.close()
            self._conn.close()

    def get_channel(self) -> Channel:
        return self._channel

    def is_connected(self, health_target: str) -> bool:
        if self.TEST_MODE:
            return True
        try:
            self._channel.queue_declare(queue=health_target, passive=True)
            return True
        except Exception as e:
            self._log.error(e)
            return False
