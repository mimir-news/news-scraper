# Internal modules
from app.service.scoring_service import CorpusReader
from app.service.scoring_service import flatten_lists
from app.service.scoring_service import join_strings


def test_get_corpus():
    reader = CorpusReader()
    corpus = reader.read()

    for document in corpus:
        assert isinstance(document, str)
        assert len(document) > 0


def test_get_stopwords():
    reader = CorpusReader()
    stopwords = reader.get_stopwords()

    for sw in stopwords:
        print(sw)
        assert isinstance(sw, str)


def test_flatten_list():
    list_of_lists_1 = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    list_of_lists_2 = [
        [9, 10, 11],
        [12, 13, 14],
        [15, 16, 17]
    ]

    inception_list = [
        list_of_lists_1,
        list_of_lists_2
    ]

    nested_list = flatten_lists(inception_list)
    flat_list = flatten_lists(nested_list)
    assert len(nested_list) == 6
    assert len(flat_list) == 18
    for index, member in enumerate(flat_list):
        assert index == member


def test_join_strings():
    strings = ['a', 'b', 'c']
    assert join_strings(strings) == 'a b c'
