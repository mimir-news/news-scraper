# Standard library
import logging

# Internal modules
from app.models import ScrapeTarget, Article


class ScrapingService:

    _log = logging.getLogger('ScrapingService')

    def get_article(self, target: ScrapeTarget) -> Article:
        return Article(
            url=target.url,
            article_id=target.article_id)
