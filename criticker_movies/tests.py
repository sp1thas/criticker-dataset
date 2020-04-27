import unittest
from criticker_movies.criticker_movies.spiders.movies_spider import MoviesSpiderSpider


class ScrapyTests(unittest.TestCase):

    def setUp(self) -> None:
        self.crawler = MoviesSpiderSpider()

    def test_slugifier(self):
        self.assertEqual(
            self.crawler.slugify('asd d[]'),
            'asd_d'
        )

    def test_extract_label(self):
        self.assertEqual(
            self.crawler.extract_label_from_id('fi_info_name'),
            'name'
        )

    def test_extract_id(self):
        url = 'https://www.criticker.com/film/10000-BC/'
        self.assertEqual(
            self.crawler.extract_uid_from_url(url),
            'ecba80b4d99d7c6a81b28119d82754ae'
        )
