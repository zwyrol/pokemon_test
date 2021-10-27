from django.test import TestCase
from app.pokemon.storage import (
    PokemonStorage,
    PokemonNotFoundException,
    PokemonStatsNotFoundException,
    PokemonAbilityStorage,
    PokemonStatsStorage
)

from app.abilities.storage import AbilitiesStorage


class PokemonTestCase(TestCase):

    def setUp(self):
        pass

    def test_pokemon_storage_creating_and_getting(self):
        storage = PokemonStorage()

        pokemon_name = 'test'
        pokemon_url = 'test-url'

        with self.assertRaises(PokemonNotFoundException):
            storage.get_pokemon_by_name(pokemon_name)

        storage.create(pokemon_name, pokemon_url)

        pokemon = storage.get_pokemon_by_name(pokemon_name)

        self.assertEquals(pokemon.name, pokemon_name)
        self.assertEquals(pokemon.url, pokemon_url)

    def test_pokemon_storage_creating_or_getting(self):
        storage = PokemonStorage()

        pokemon_name = 'test'
        pokemon_url = 'test-url'

        with self.assertRaises(PokemonNotFoundException):
            storage.get_pokemon_by_name(pokemon_name)

        pokemon1 = storage.get_or_create(pokemon_name, pokemon_url)
        pokemon2 = storage.get_or_create(pokemon_name, pokemon_url)

        self.assertEquals(pokemon1.name, pokemon2.name)
        self.assertEquals(pokemon1.url, pokemon2.url)
        self.assertEquals(pokemon1.id, pokemon2.id)

    def test_pokemon_ability_storage_creating_and_getting(self):
        pokemon_storage = PokemonStorage()
        ability_storage = AbilitiesStorage()
        pokemon_ability_storage = PokemonAbilityStorage()

        pokemon = pokemon_storage.create('test', 'test-url')
        ability1 = ability_storage.create('test-ability1', 'test-ability-url')
        ability2 = ability_storage.create('test-ability2', 'test-ability-url')

        self.assertEquals(pokemon_ability_storage.get_by_pokemon(pokemon), [])

        pokemon_ability_storage.create(pokemon=pokemon, ability=ability1)
        pokemon_ability_storage.create(pokemon=pokemon, ability=ability2)

        pokemon_abilities = pokemon_ability_storage.get_by_pokemon(pokemon)

        self.assertEquals(len(pokemon_abilities), 2)

        for ability, ability_from_db in zip([ability1, ability2], pokemon_abilities):
            self.assertEquals(ability.id, ability_from_db.id)
            self.assertEquals(ability.name, ability_from_db.name)
            self.assertEquals(ability.url, ability_from_db.url)

    def test_pokemon_stats_storage_creating_and_getting(self):
        pokemon_storage = PokemonStorage()
        pokemon_stats_storage = PokemonStatsStorage()

        pokemon = pokemon_storage.create('test', 'test-url')
        with self.assertRaises(PokemonStatsNotFoundException):
            pokemon_stats_storage.get_by_pokemon(pokemon)

        pokemon = pokemon_storage.create('test', 'test-url')

        pokemon_stats_storage.create(pokemon=pokemon, height=30, weight=40, base_experience=500)
        pokemon_stats = pokemon_stats_storage.get_by_pokemon(pokemon)

        self.assertEquals(pokemon_stats.pokemon, pokemon)
        self.assertEquals(pokemon_stats.height, 30)
        self.assertEquals(pokemon_stats.weight, 40)
        self.assertEquals(pokemon_stats.base_experience, 500)

    def test_pokemon_ability_storage_removing_all(self):
        pokemon_storage = PokemonStorage()
        ability_storage = AbilitiesStorage()
        pokemon_ability_storage = PokemonAbilityStorage()

        pokemon = pokemon_storage.create('test', 'test-url')
        ability1 = ability_storage.create('test-ability1', 'test-ability-url')
        ability2 = ability_storage.create('test-ability2', 'test-ability-url')

        self.assertEquals(pokemon_ability_storage.get_by_pokemon(pokemon), [])

        pokemon_ability_storage.create(pokemon=pokemon, ability=ability1)
        pokemon_ability_storage.create(pokemon=pokemon, ability=ability2)

        pokemon_abilities = pokemon_ability_storage.get_by_pokemon(pokemon)

        self.assertEquals(len(pokemon_abilities), 2)

        pokemon_ability_storage.remove_all(pokemon)
        pokemon_abilities = pokemon_ability_storage.get_by_pokemon(pokemon)

        self.assertEquals(len(pokemon_abilities), 0)

    def test_pokemon_stats_storage_removing(self):
        pokemon_storage = PokemonStorage()
        pokemon_stats_storage = PokemonStatsStorage()

        pokemon = pokemon_storage.create('test', 'test-url')

        pokemon_stats_storage.create(pokemon=pokemon, height=30, weight=40, base_experience=500)
        pokemon_stats = pokemon_stats_storage.get_by_pokemon(pokemon)

        self.assertEquals(pokemon_stats.pokemon, pokemon)

        pokemon_stats_storage.remove(pokemon)

        with self.assertRaises(PokemonStatsNotFoundException):
            pokemon_stats_storage.get_by_pokemon(pokemon)
