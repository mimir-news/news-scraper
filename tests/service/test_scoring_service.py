# Standard library
from datetime import datetime

# Internal modules
from app.models import Article, Subject
from app.service import ScoringService


def test_scoring_service():
    article = Article(
        id='a-id',
        url='a-url',
        title='Apple’s Social Network',
        body=read_article_body(),
        keywords=[],
        date=datetime.utcnow())
    subjects = [
        Subject(id='s-0', symbol='AAPL', name='Apple inc.',
                score=0.0, article_id='a-id'),
        Subject(id='s-1', symbol='GOOG', name='Alphabet inc.',
                score=0.0, article_id='a-id')
    ]

    expected_scores = [
        ('s-0', 0.37470489668959894),
        ('s-1', 0.004385360758615228)
    ]

    scorer = ScoringService()
    scored_subjects = scorer.score(article, subjects)

    assert len(scored_subjects) == len(expected_scores)
    for i, ssub in enumerate(scored_subjects):
        expected_id, expected_score = expected_scores[i]
        assert ssub.id == expected_id
        assert ssub.score == expected_score


def read_article_body() -> str:
    with open('./testdata/article_body.txt', 'r') as f:
        return f.read()
