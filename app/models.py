# Standard library
import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class DTO(metaclass=ABCMeta):
    """DTO is the abtract baseclass of classes that can 
    turn themselves from an into a dict.
    """

    @abstractmethod
    def asdict(self) -> Dict[str, Any]:
        """Retruns a dictionary representation of an object."""

    @abstractmethod
    def fromdict(self, raw: Dict[str, Any]) -> 'DTO':
        """Turns a dictionary into an object of the DTO implementation."""


@dataclass
class Subject(DTO):
    id: str
    symbol: str
    name: str
    score: float
    article_id: str

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
    article_date: datetime

    def asdict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'body': self.body,
            'keywords': self.keywords,
            'articleDate': self.article_date
        }

    @staticmethod
    def fromdict(raw: Dict[str, Any]) -> 'Article':
        try:
            return Article(
                id=raw['id'],
                url=raw['url'],
                title=raw['title'],
                body=raw['body'],
                keywords=raw['keywords'],
                article_date=raw['articleDate'])
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
    error_message = json.dumps({
        'id': str(uuid4()),
        'message': str(error)
    })
    return ValueError(error_message)
