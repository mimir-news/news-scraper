# Standard library
import logging
from datetime import datetime

# 3rd party modules
import newspaper

# Internal modules
from app.models import ScrapeTarget, Article


class ScrapingService:

    _log = logging.getLogger('ScrapingService')

    def get_article(self, target: ScrapeTarget) -> Article:
        if target.is_scraped():
            return target.article()
        article = newspaper.Article(target.url)
        article.download()
        article.parse()
        article.nlp()

        article_date = article.publish_date or datetime.utcnow()
        return Article(
            id=target.article_id,
            url=target.url,
            title=article.title,
            body=article.text,
            keywords=article.keywords,
            date=article_date)
