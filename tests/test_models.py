# 3rd party modules
import pytest

# Internal modules
from app.models import Subject
from app.models import Article


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

    assert article.describe() == 'a-title a-body k-0 k-1'

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
