# Standard library
import logging
from concurrent.futures import ThreadPoolExecutor

# Internal modules
from app.models import ScrapeTarget, ScrapedArticle
from app.service import ScrapingService, ScoringService


class Worker:

    _log = logging.getLogger('Worker')

    def __init__(self,
                 scraper: ScrapingService,
                 scorer: ScoringService) -> None:
        self._scraper = scraper
        self._scorer = scorer

    def scrape_and_rank(self, target: ScrapeTarget) -> None:
        article = self._scraper.get_article(target)
        subjects = self._scorer.score(article, target.subjects)
        result = ScrapedArticle(
            article=article,
            subjects=subjects,
            referer=target.referer)
        self._log.info(result)
