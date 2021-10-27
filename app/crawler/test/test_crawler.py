from django.test import TestCase
from unittest.mock import patch
import random
import string
from app.crawler import Crawler, CrawlerApiException, CrawlerPokemonNotFoundException


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


class ResponseGenerator:
    @staticmethod
    def generate_pokemon():
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(5, 10))

        return {'name': name, 'url': f'https://pokeapi.co/api/v2/pokemon/{name}'}

    @staticmethod
    def generate_pokemons(number):
        return [ResponseGenerator.generate_pokemon() for _ in range(0, number)]

    @staticmethod
    def generate_pokemon_abilities():
        return [{'ability': {'name': 'blaze', 'url': 'https://pokeapi.co/api/v2/ability/66/'}},
                {'ability': {'name': 'solar-power', 'url': 'https://pokeapi.co/api/v2/ability/94/'}}]

    @staticmethod
    def generate_pokemons_list_response(pokemons_number, status_code=200):
        pokemons = ResponseGenerator.generate_pokemons(pokemons_number)

        return MockResponse(data={'count': len(pokemons), 'results': pokemons}, status_code=status_code)

    @staticmethod
    def generate_single_pokemon_response(status_code=200):
        return MockResponse(data={'abilities': ResponseGenerator.generate_pokemon_abilities(),
                                  'base_experience': random.randint(1, 500),
                                  'height': random.randint(1, 100),
                                  'weight': random.randint(1, 50)}, status_code=status_code)


class CrawlerTestCase(TestCase):

    def setUp(self):
        pass

    @patch('app.crawler.requests.get')
    def test_getting_pokemons(self, requests_get):
        pokemons_number = 1000
        pokemons_from_mock = ResponseGenerator.generate_pokemons_list_response(pokemons_number=pokemons_number, status_code=200)
        requests_get.return_value = pokemons_from_mock
        crawler = Crawler()
        pokemons = crawler.get_pokemons()

        self.assertEqual(len(pokemons), pokemons_number)

        for pfc, pfm in zip(pokemons, pokemons_from_mock.data['results']):
            self.assertEqual(pfc['name'], pfm['name'])
            self.assertEqual(pfc['url'], pfm['url'])

    @patch('app.crawler.requests.get')
    def test_getting_api_issue(self, requests_get):
        error_statuses = [403, 404, 405]

        for status_code in error_statuses:
            pokemons_from_mock = ResponseGenerator.generate_pokemons_list_response(pokemons_number=1, status_code=status_code)
            requests_get.return_value = pokemons_from_mock
            crawler = Crawler()

            with self.assertRaises(CrawlerApiException):
                crawler.get_pokemons()

    @patch('app.crawler.requests.get')
    def test_getting_single_pokemon(self, requests_get):
        pokemon_response = ResponseGenerator.generate_single_pokemon_response()

        requests_get.return_value = pokemon_response

        crawler = Crawler()
        cpokemon = crawler.get_pokemon('test')

        self.assertEquals(cpokemon['abilities'], pokemon_response.data['abilities'])
        self.assertEquals(cpokemon['height'], pokemon_response.data['height'])
        self.assertEquals(cpokemon['weight'], pokemon_response.data['weight'])
        self.assertEquals(cpokemon['base_experience'], pokemon_response.data['base_experience'])

    @patch('app.crawler.requests.get')
    def test_getting_single_pokemon_not_found(self, requests_get):
        pokemon_response = ResponseGenerator.generate_single_pokemon_response(status_code=404)

        requests_get.return_value = pokemon_response

        with self.assertRaises(CrawlerPokemonNotFoundException):
            crawler = Crawler()
            crawler.get_pokemon('test')

    @patch('app.crawler.requests.get')
    def test_getting_single_pokemon_api_error(self, requests_get):
        error_statuses = [403, 405]
        for status_code in error_statuses:
            pokemon_response = ResponseGenerator.generate_single_pokemon_response(status_code=status_code)

            requests_get.return_value = pokemon_response

            with self.assertRaises(CrawlerApiException):
                crawler = Crawler()
                crawler.get_pokemon('test')
