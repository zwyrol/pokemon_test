import requests


class CrawlerApiException(Exception):
    pass


class CrawlerPokemonNotFoundException(CrawlerApiException):
    pass


class Crawler:
    def __init__(self):
        self.api_url = 'https://pokeapi.co/api/v2'

    def get_pokemons(self):
        # TODO: Get pokemons by batches as number is more than 1000
        r = requests.get(f'{self.api_url}/pokemon?limit=1000')

        if r.status_code != 200:
            raise CrawlerApiException("Can't fetch pokemons list.")

        return r.json()['results']

    def get_pokemon(self, name):
        r = requests.get(f'{self.api_url}/pokemon/{name}')

        if r.status_code == 404:
            raise CrawlerPokemonNotFoundException(f"Pokemon {name} not found")
        elif r.status_code != 200:
            raise CrawlerApiException(f"Can't fetch pokemon {name}")

        return r.json()

    def get_pokemons_info(self):
        pass
        # TODO: This function should run 'get_pokemon' function in Threads for improving performance

