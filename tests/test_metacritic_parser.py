import json
import unittest

import requests
import requests_mock

from metacritic.parser import get_json_data

from .utils import load_test_asset


def set_mock_data(m):
    """
    this is helper function. load mock data (real metacritic pages. 20190902)
    """
    m.register_uri(
        'GET', 'https://www.metacritic.com/browse/games/release-date/available/ps4/metascore',
        [
            {'text': load_test_asset('page.html.gz')},
            {'text': load_test_asset('page1.html.gz')},
            {'text': load_test_asset('page2.html.gz')},
            {'text': load_test_asset('page3.html.gz')},
            {'text': load_test_asset('page4.html.gz')},
            {'text': load_test_asset('page5.html.gz')},
            {'text': load_test_asset('page6.html.gz')},
            {'text': load_test_asset('page7.html.gz')},
            {'text': load_test_asset('page8.html.gz')},
            {'text': load_test_asset('page9.html.gz')},
            {'text': load_test_asset('page10.html.gz')},
        ]
    )


class MetacriticParserTestCase(unittest.TestCase):
    @requests_mock.Mocker()
    def test_response_is_empty_on_nonstandard_page(self, m):
        """
        test any html page could be processed (maintenance / not found / 503 / etc)
        non standard page => no data (empty list)
        """
        m.register_uri(
            'GET', 'https://www.metacritic.com/browse/games/release-date/available/ps4/metascore',
            text=load_test_asset('example.com.html.gz')
        )

        self.assertTrue(len(json.loads(get_json_data())) == 0)

    @requests_mock.Mocker()
    def test_network_error_handled_properly(self, m):
        """
        test network errors handled properly.
        in case of network error return entry with error status
        """
        m.register_uri(
            'GET', 'https://www.metacritic.com/browse/games/release-date/available/ps4/metascore',
            exc=requests.exceptions.ConnectTimeout
        )
        data = json.loads(get_json_data())
        self.assertEqual(1, len(data) == 1)
        self.assertTrue('error' in data[0])
        self.assertEqual(data[0]['error'], 'failed to establish a connection')

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed(self, m):
        """
        mock metacritic pages and run parser on real data.
        this should produce json list with title, score pairs for each game presented in source pages

        [
          {'title': 'Red Dead Redemption 2', 'score': '97'},
          ...
          {'title': 'Orc Slayer', 'score': '15'}
        ]
        """
        set_mock_data(m)
        data = json.loads(get_json_data())
        # print('total:', len(data))
        # print(data)
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 2037)
        for entry in data:
            self.assertTrue('title' in entry)
            self.assertTrue(type(entry['title']) == str)
            self.assertTrue('score' in entry)
            self.assertTrue(type(entry['score']) == str)

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed_key_search_rdr2(self, m):
        """
        mock metacritic pages and run parser. subject: 'Red Dead Redemption 2'
        """
        set_mock_data(m)
        search_query = 'Red Dead Redemption 2'
        data = json.loads(get_json_data(key_search=search_query))
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 1)
        self.assertTrue('title' in data[0])
        self.assertEqual(data[0]['title'], 'Red Dead Redemption 2')
        self.assertTrue('score' in data[0])
        self.assertEqual(data[0]['score'], '97')

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed_key_search_rdr2_partial_match(self, m):
        """
        mock metacritic pages and run parser. subject: 'Red Dead' ('Red Dead Redemption 2')
        partial title provided but there is game with similar title. should return it
        """
        set_mock_data(m)
        search_query = 'Red Dead'
        data = json.loads(get_json_data(key_search=search_query))
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 1)
        self.assertTrue('title' in data[0])
        self.assertEqual(data[0]['title'], 'Red Dead Redemption 2')
        self.assertTrue(search_query in data[0]['title'])
        self.assertTrue('score' in data[0])
        self.assertEqual(data[0]['score'], '97')

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed_key_search_witcher(self, m):
        """
        mock metacritic pages and run parser. subject: 'Witcher' ('Red Dead Redemption 2')
        partial title provided but there is multiple games with similar title. should return every match
        [
            {'title': 'The Witcher 3: Wild Hunt', 'score': '92'},
            {'title': 'The Witcher 3: Wild Hunt - Blood and Wine', 'score': '91'},
            {'title': 'The Witcher 3: Wild Hunt - Hearts of Stone', 'score': '90'},
            {'title': 'Thronebreaker: The Witcher Tales', 'score': '79'}
        ]
        """
        set_mock_data(m)
        search_query = 'Witcher'
        data = json.loads(get_json_data(key_search=search_query))
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 4)
        for entry in data:
            self.assertTrue('title' in entry)
            self.assertTrue(type(entry['title']) == str)
            self.assertTrue('score' in entry)
            self.assertTrue(type(entry['score']) == str)
            self.assertTrue(search_query in entry['title'])

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed_key_search_orc_slayer(self, m):
        """
        mock metacritic pages and run parser. subject: 'Orc Slayer'
        """
        set_mock_data(m)
        search_query = 'Orc Slayer'
        data = json.loads(get_json_data(key_search=search_query))
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 1)
        self.assertTrue('title' in data[0])
        self.assertEqual(data[0]['title'], 'Orc Slayer')
        self.assertTrue(search_query in data[0]['title'])
        self.assertTrue('score' in data[0])
        self.assertEqual(data[0]['score'], '15')

    @requests_mock.Mocker()
    def test_metacritic_pages_parsed_key_search_no_such_game(self, m):
        """
        mock metacritic pages and run parser. subject: 'FOOBAR Adventure 40k'
        this game not exists so no results expected (empty list)
        """
        set_mock_data(m)
        search_query = 'FOOBAR Adventure 40k'
        data = json.loads(get_json_data(key_search=search_query))
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
