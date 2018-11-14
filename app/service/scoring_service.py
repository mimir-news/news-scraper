# Standard library
import itertools
import logging
import os
from typing import List

# 3rd party modules
import stop_words
from nltk.corpus import brown

# Internal modules
from app.models import Article, Subject


class ScoringService:

    _log = logging.getLogger('ScoringService')

    def __init__(self) -> None:
        _corpus_reader = CorpusReader()
        self.CORPUS = _corpus_reader.create()
        self.STOPWORDS = _corpus_reader.get_stopwords()

    def score(self, article: Article, subjects: List[Subject]) -> List[Subject]:
        return subjects

    def _create_corpus(self) -> List[str]:
        BROWN_CATEGORIES = ['news', 'editorial']
        return brown.words(categories=BROWN_CATEGORIES)


class CorpusReader:

    CATEGORIES = ['news', 'editorial']

    def create(self) -> List[str]:
        fileids = self._get_brown_fileids()
        return [self._parse_file(id) for id in fileids]

    def get_stopwords(self) -> List[str]:
        return stop_words.get_stop_words(language='en')

    def _parse_file(self, fileid: str) -> str:
        documents = brown.sents(fileid)
        flattened_documents = flatten_lists(documents)
        flattened_sentences = flatten_lists(flattened_documents)
        sentences = [join_strings(sent) for sent in flattened_sentences]
        return join_strings(sentences)

    def _get_brown_fileids(self) -> List[str]:
        return brown.fileids(categories=self.CATEGORIES)


def flatten_lists(base_list: List[List]) -> List:
    return list(itertools.chain(base_list))


def join_strings(words: List[str]) -> str:
    return " ".join(words)
