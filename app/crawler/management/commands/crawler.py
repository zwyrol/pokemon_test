from django.core.management.base import BaseCommand, CommandError
from app.crawler import Crawler, CrawlerApiException
from app.pokemon.storage import PokemonStorage, PokemonStatsStorage, PokemonAbilityStorage
from app.abilities.storage import AbilitiesStorage


class Command(BaseCommand):
    help = 'Running Crawler and fetching pokemons'

    def add_arguments(self, parser):
        pass

    def _parse_stats(self, pokemon_info):
        return {'height': pokemon_info['height'],
                'weight': pokemon_info['weight'],
                'base_experience': pokemon_info['base_experience']}

    def _parse_abilities(self, crawler_abilities):
        storage = AbilitiesStorage()

        abilities = []
        for cability in crawler_abilities:
            abilities.append(storage.get_or_create(name=cability['ability']['name'], url=cability['ability']['url']))

        return abilities

    def _create_abilities(self, pokemon, abilities):
        pokemon_ability_storage = PokemonAbilityStorage()

        for ability in abilities:
            pokemon_ability_storage.create(pokemon=pokemon, ability=ability)

    def handle(self, *args, **options):
        c = Crawler()
        pokemon_storage = PokemonStorage()
        pokemon_ability_storage = PokemonAbilityStorage()
        pokemon_stats_storage = PokemonStatsStorage()

        try:
            pokemons = c.get_pokemons()

            for pokemon_data in pokemons:
                pokemon = pokemon_storage.get_or_create(pokemon_data['name'], pokemon_data['url'])

                pokemon_info = c.get_pokemon(pokemon.name)
                pokemon_ability_storage.remove_all(pokemon)
                pokemon_stats_storage.remove(pokemon)

                abilities = self._parse_abilities(pokemon_info['abilities'])
                stats = self._parse_stats(pokemon_info)
                self._create_abilities(pokemon, abilities)
                pokemon_stats_storage.create(pokemon=pokemon,
                                             height=stats['height'],
                                             weight=stats['weight'],
                                             base_experience=stats['base_experience'])
        except CrawlerApiException:
            pass
