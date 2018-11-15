# Standard library
import itertools
import logging
import os
from typing import List, Any

# 3rd party modules
import stop_words
from nltk.corpus import brown
from scipy.sparse.csr import csr_matrix as ScipyMatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Internal modules
from app.models import Article, Subject


class ScoringService:
    """Service responsible for scoring subjects against an article."""

    _log = logging.getLogger('ScoringService')

    def __init__(self) -> None:
        _corpus_reader = CorpusReader()
        self.CORPUS = _corpus_reader.read()
        self.STOPWORDS = _corpus_reader.get_stopwords()
        self._log.info("Corpus and stopwords successfully loaded.")

    def score(self, article: Article, subjects: List[Subject]) -> List[Subject]:
        """Scores subjects against an article by comparing how simliar they are.

        :param article: Article to score against.
        :param subjects: List of subjects to score.
        :return: List of subjects with scores.
        """
        scores = self._calc_scores(article, subjects)
        for i, score in enumerate(scores):
            subjects[i].score = score
        return subjects

    def _calc_scores(self, article: Article, subjects: List[Subject]) -> List[float]:
        """Computes scores by calculating tfidf weighted cosine similarity.

        :param article: Article to score against.
        :param subjects: List of subjects to score.
        :return: List of scores.
        """
        tfidf_matrix = self._build_tfidf_matrix(article, subjects)
        no_subjects = len(subjects)
        subject_vectors = tfidf_matrix[0:no_subjects]
        article_vector = tfidf_matrix[no_subjects:no_subjects+1]
        similarities = cosine_similarity(subject_vectors, article_vector)
        return [float(s) for s in similarities]

    def _build_tfidf_matrix(self, article: Article, subjects: List[Subject]) -> ScipyMatrix:
        """Builds a tfidf matrix based on the article, the subjects and the base corpus.

        :param article: Article to score against.
        :param subjects: List of subjects to score.
        :return: Tfidf matrix.
        """
        article_desc = [article.describe()]
        subject_descriptions = [s.describe() for s in subjects]
        vectorizer = TfidfVectorizer(stop_words=self.STOPWORDS)
        documents: List[str] = subject_descriptions + \
            article_desc + self.CORPUS
        return vectorizer.fit_transform(documents)


class CorpusReader:
    """Utility class for reading of text corpus used for ranking."""

    CATEGORIES = ['news', 'editorial']

    def read(self) -> List[str]:
        """Parses and formats text corpus.

        :return: List of strings each representing a document.
        """
        fileids = self._get_brown_fileids()
        return [self._parse_file(id) for id in fileids]

    def get_stopwords(self) -> List[str]:
        """Gets stopwords to filter out for ranking.

        :return: List of stopwords.
        """
        return stop_words.get_stop_words(language='en')

    def _parse_file(self, fileid: str) -> str:
        """Parses a file in the brown corpus and returns it as a string.

        :param fileid: Id of the file to parse.
        :return: Parsed file as a string.
        """
        documents = brown.sents(fileid)
        flattened_documents = flatten_lists(documents)
        flattened_sentences = flatten_lists(flattened_documents)
        sentences = [join_strings(sent) for sent in flattened_sentences]
        return join_strings(sentences)

    def _get_brown_fileids(self) -> List[str]:
        """Gets the relevant file ids in the brown corpus used for ranking.

        :return: List of fileid strings.
        """
        return brown.fileids(categories=self.CATEGORIES)


def flatten_lists(base_list: List[List]) -> List:
    """Flattens a list of list to a list.

    :param base_list: List of lists.
    :return: Flattened list.
    """
    return list(itertools.chain.from_iterable(base_list))


def join_strings(words: List[str]) -> str:
    """Joins a list for strings into a single string.

    :param words: Words to join.
    :return: Joined string.
    """
    return " ".join(words)
