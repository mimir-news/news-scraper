# Standard library
import json
from abc import ABCMeta, abstractmethod, abstractstaticmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

# Internal modules
from app.util import wrap_error_message, date_to_str, str_to_date


class DTO(metaclass=ABCMeta):
    """DTO is the abtract baseclass of classes that can 
    turn themselves from an into a dict.
    """

    @abstractmethod
    def asdict(self) -> Dict[str, Any]:
        """Retruns a dictionary representation of an object."""

    @abstractstaticmethod
    def fromdict(self, raw: Dict[str, Any]) -> 'DTO':
        """Turns a dictionary into an object of the DTO implementation."""


@dataclass
class Subject(DTO):
    id: str
    symbol: str
    name: str
    score: float
    article_id: str

    def describe(self) -> str:
        """Creats a string describing the subject that can be ranked against.

        :return: String describing the subject.
        """
        return f'{self.symbol} {self.name}'

    def asdict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'score': self.score,
            'articleId': self.article_id
        }

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'Subject':
        try:
            return Subject(
                id=raw['id'],
                symbol=raw['symbol'],
                name=raw['name'],
                score=raw['score'],
                article_id=raw['articleId'])
        except KeyError as e:
            raise wrap_key_error(e)


@dataclass(frozen=True)
class Referer(DTO):
    id: str
    external_id: str
    follower_count: int
    article_id: str

    def asdict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'externalId': self.external_id,
            'followerCount': self.follower_count,
            'articleId': self.article_id
        }

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'Referer':
        try:
            return Referer(
                id=raw['id'],
                external_id=raw['externalId'],
                follower_count=raw['followerCount'],
                article_id=raw['articleId'])
        except KeyError as e:
            raise wrap_key_error(e)


@dataclass(frozen=True)
class Article(DTO):
    id: str
    url: str
    title: str
    body: str
    keywords: List[str]
    date: datetime

    def asdict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'body': self.body,
            'keywords': self.keywords,
            'articleDate': date_to_str(self.date)
        }

    def describe(self) -> str:
        """Creates a string describing the article that can be ranked against.

        :return: String describing the article.
        """
        joined_keywords = " ".join(self.keywords)
        return f'{self.title} {self.body} {joined_keywords}'

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'Article':
        try:
            return Article(
                id=raw['id'],
                url=raw['url'],
                title=raw['title'],
                body=raw['body'],
                keywords=raw['keywords'],
                date=str_to_date(raw['articleDate']))
        except KeyError as e:
            raise wrap_key_error(e)


@dataclass
class ScrapeTarget:
    url: str
    subjects: List[Subject]
    referer: Referer
    title: str
    body: str
    article_id: str

    def asdict(self) -> Dict[str, Any]:
        return {
            'url': self.url,
            'subjects': [sub.asdict() for sub in self.subjects],
            'referer': self.referer.asdict(),
            'title': self.title,
            'body': self.body,
            'articleId': self.article_id
        }

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'ScrapeTarget':
        try:
            return ScrapeTarget(
                url=raw['url'],
                subjects=[Subject.fromdict(sub) for sub in raw['subjects']],
                referer=Referer.fromdict(raw['referer']),
                title=raw['title'],
                body=raw['body'],
                article_id=raw['articleId'])
        except KeyError as e:
            raise wrap_key_error(e)


@dataclass
class ScrapedArticle:
    article: Article
    subjects: List[Subject]
    referer: Referer

    def asdict(self) -> Dict[str, Any]:
        return {
            'article': self.article.asdict(),
            'subjects': [sub.asdict() for sub in self.subjects],
            'referer': self.referer.asdict()
        }

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'ScrapedArticle':
        try:
            return ScrapedArticle(
                article=Article.fromdict(raw['article']),
                subjects=[Subject.fromdict(sub) for sub in raw['subjects']],
                referer=Referer.fromdict(raw['referer']))
        except KeyError as e:
            raise wrap_key_error(e)


def wrap_key_error(error: KeyError) -> ValueError:
    return ValueError(wrap_error_message(error))
