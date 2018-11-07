# Standard library
import logging
from concurrent.futures import ThreadPoolExecutor

# Internal modules
from app.models import ScrapeTarget, ScrapedArticle
from app.service import MQClient, MQDeliver, MessageHandler
from app.service import ScrapingService, ScoringService


class Worker(MessageHandler):

    _log = logging.getLogger('Worker')

    def __init__(self,
                 scraper: ScrapingService,
                 scorer: ScoringService,
                 mq_client: MQClient) -> None:
        self._scraper = scraper
        self._scorer = scorer
        self._mq_client = mq_client

    def handle_scrape_target(self, target: ScrapeTarget, mq_method: MQDeliver) -> None:
        try:
            scraped_article = self._scrape_and_rank(target)
            self._mq_client.send(scraped_article)
            self._mq_client.ack(mq_method)
        except Exception as e:
            self._log.error(str(e))
            self._mq_client.reject(mq_method)

    def _scrape_and_rank(self, target: ScrapeTarget) -> ScrapedArticle:
        article = self._scraper.get_article(target)
        subjects = self._scorer.score(article, target.subjects)
        return ScrapedArticle(
            article=article,
            subjects=subjects,
            referer=target.referer)
