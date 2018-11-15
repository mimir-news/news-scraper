# 3rd party modules
import pytest
from datetime import datetime

# Internal modules
from app.models import Subject
from app.models import Article
from app.models import Referer
from app.models import ScrapeTarget
from app.models import ScrapedArticle


def test_subject():
    raw = {
        'id': 'sub-id',
        'symbol': 'sub-symbol',
        'name': 'sub-name',
        'score': 0.1,
        'articleId': 'a-id'
    }
    subject = Subject.fromdict(raw)
    assert subject.id == 'sub-id'
    assert subject.score == 0.1

    assert subject.describe() == 'sub-symbol sub-name'

    with pytest.raises(ValueError):
        wrong_raw = {
            'id': 'sub-id',
            'symbol': 'sub-symbol',
            'name': 'sub-name'
        }
        Subject.fromdict(wrong_raw)


def test_article():
    raw = {
        'id': 'a-id',
        'url': 'a-url',
        'title': 'a-title',
        'body': 'a-body',
        'keywords': ['k-0', 'k-1'],
        'articleDate': '2018-11-14 10:10:10'
    }
    article = Article.fromdict(raw)
    assert article.id == 'a-id'
    assert article.date.year == 2018
    assert article.date.month == 11
    assert article.date.day == 14

    assert article.describe() == 'a-title a-body'

    with pytest.raises(ValueError):
        wrong_raw = {
            'id': 'a-id',
            'url': 'a-url',
            'keywords': ['k-0', 'k-1'],
            'articleDate': '2018-11-14 10:10:10'
        }
        article.fromdict(wrong_raw)

    with pytest.raises(ValueError):
        wrong_raw = {
            'id': 'a-id',
            'url': 'a-url',
            'title': 'a-title',
            'body': 'a-body',
            'keywords': ['k-0', 'k-1'],
            'articleDate': '18-11-14T10:10:10'
        }
        article.fromdict(wrong_raw)


def test_scrape_target():
    raw = {
        'url': 'target-url',
        'subjects': [
            {
                'id': 'sub-id',
                'symbol': 'sub-symbol',
                'name': 'sub-name',
                'score': 0.1,
                'articleId': 'a-id'
            }
        ],
        'referer': {
            'id': 'r-id',
            'externalId': 'e-id',
            'followerCount': 100,
            'articleId': 'a-id'
        },
        'title': 'a-title',
        'body': 'a-body',
        'articleId': 'a-id'
    }
    scrape_target = ScrapeTarget.fromdict(raw)

    assert scrape_target.url == 'target-url'
    assert len(scrape_target.subjects) == 1
    assert scrape_target.referer.id == 'r-id'
    assert scrape_target.is_scraped()

    raw['title'] = None
    raw['body'] = None

    scrape_target_w_none = ScrapeTarget.fromdict(raw)
    assert not scrape_target_w_none.is_scraped()

    raw['title'] = ''
    raw['body'] = ''

    scrape_target_w_empty = ScrapeTarget.fromdict(raw)
    assert not scrape_target_w_empty.is_scraped()


def test_invalid_scrape_target():
    invalid_raw = {
        'url': 'target-url',
        'title': '',
        'body': '',
        'articleId': 'a-id'
    }
    with pytest.raises(ValueError):
        ScrapeTarget.fromdict(invalid_raw)


def test_scrape_target_to_article_conversion():
    target = ScrapeTarget(
        url='target-url',
        subjects=[
            Subject(id='s-id', symbol='symbol', name='name',
                    score=0.0, article_id='a-id')
        ],
        referer=Referer(id='r-id', external_id='e-id',
                        follower_count=100, article_id='a-id'),
        title='a-title',
        body='a-body',
        article_id='a-id'
    )
    article = target.article()
    assert article.id == target.article_id
    assert article.url == target.url

    invalid_target = ScrapeTarget(
        url='target-url',
        subjects=[
            Subject(id='s-id', symbol='symbol', name='name',
                    score=0.0, article_id='a-id')
        ],
        referer=Referer(id='r-id', external_id='e-id',
                        follower_count=100, article_id='a-id'),
        title=None,
        body=None,
        article_id='a-id'
    )
    with pytest.raises(ValueError):
        invalid_target.article()


def test_scraped_article_serialization():
    scraped_article = ScrapedArticle(
        article=Article(
            id='a-id',
            url='target-url',
            title='a-title',
            body='a-body',
            keywords=[
                'k-0', 'k-1'
            ],
            date=datetime.utcnow()),
        subjects=[
            Subject(
                id='s-id',
                symbol='symbol',
                name='name',
                score=0.0,
                article_id='a-id')
        ],
        referer=Referer(
            id='r-id',
            external_id='e-id',
            follower_count=100,
            article_id='a-id')
    )
    sa_dict = scraped_article.asdict()
    sa_dict['article']['id'] == 'a-id'


def test_failing_scraped_article_serialization():
    missing_date_article = ScrapedArticle(
        article=Article(
            id='a-id',
            url='target-url',
            title='a-title',
            body='a-body',
            keywords=[
                'k-0', 'k-1'
            ],
            date=None),
        subjects=[
            Subject(
                id='s-id',
                symbol='symbol',
                name='name',
                score=0.0,
                article_id='a-id')
        ],
        referer=Referer(
            id='r-id',
            external_id='e-id',
            follower_count=100,
            article_id='a-id')
    )
    with pytest.raises(AttributeError):
        missing_date_article.asdict()

    with pytest.raises(TypeError):
        ScrapedArticle(
            article=Article(
                id='a-id',
                url='target-url',
                title='a-title',
                body='a-body',
                keywords=[
                    'k-0', 'k-1'
                ],
                date=datetime.utcnow())
        )
