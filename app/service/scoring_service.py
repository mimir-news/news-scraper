# Standard library
import logging
from typing import List

# 3rd party modules
from nltk.corpus import brown

# Internal modules
from app.models import Article, Subject


class ScoringService:

    _log = logging.getLogger('ScoringService')

    def __init__(self) -> None:
        self.CORPUS = self._create_corpus()

    def score(self, article: Article, subjects: List[Subject]) -> List[Subject]:
        return subjects

    def _create_corpus(self) -> List[str]:
        BROWN_CATEGORIES = ['news', 'editorial']
        return brown.words(categories=BROWN_CATEGORIES)
