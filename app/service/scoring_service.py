# Standard library
import logging
from typing import List

# Internal modules
from app.models import Article, Subject


class ScoringService:

    _log = logging.getLogger('ScoringService')

    def score(self, article: Article, subjects: List[Subject]) -> List[Subject]:
        return subjects
