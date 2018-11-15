# Standard library
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

# 3rd party modules
from pika.channel import Channel
from pika.spec import Basic as MQ

# Internal modules
from app.models import ScrapeTarget, ScrapedArticle
from app.service import MQClient, MessageHandler
from app.service import ScrapingService, ScoringService
from app.util import wrap_error_message


class Worker(MessageHandler):

    _log = logging.getLogger('Worker')

    def __init__(self,
                 scraper: ScrapingService,
                 scorer: ScoringService,
                 mq_client: MQClient) -> None:
        self._scraper = scraper
        self._scorer = scorer
        self._mq_client = mq_client

    def handle_scrape_target(self,
                             target: ScrapeTarget,
                             channel: Channel,
                             mq_method: MQ.Deliver) -> None:
        try:
            scraped_article = self._scrape_and_rank(target)
            self._mq_client.send(scraped_article)
            self._mq_client.ack(channel, mq_method)
        except Exception as e:
            self._log.error(wrap_error_message(e))
            self._mq_client.reject(channel, mq_method)

    def _scrape_and_rank(self, target: ScrapeTarget) -> ScrapedArticle:
        article = self._scraper.get_article(target)
        self._log.info(article.title)
        self._log.info(article.body)
        subjects = self._scorer.score(article, target.subjects)
        for sub in subjects:
            self._log.info(f'{sub}')
        return ScrapedArticle(
            article=article,
            subjects=subjects,
            referer=target.referer)
