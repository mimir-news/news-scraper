# Standard library
import logging
from datetime import datetime

# Internal modules
from app.models import ScrapeTarget, Article


class ScrapingService:

    _log = logging.getLogger('ScrapingService')

    def get_article(self, target: ScrapeTarget) -> Article:
        return Article(
            id=target.article_id,
            url=target.url,
            title='',
            body='',
            keywords=[],
            article_date=datetime.utcnow())
