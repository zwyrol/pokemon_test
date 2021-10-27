from django.test import TestCase
from app.abilities.storage import AbilitiesStorage, AbilitiesNotFoundException


class AbilitiesTestCase(TestCase):

    def setUp(self):
        pass

    def test_ability_storage_creating_and_getting(self):
        storage = AbilitiesStorage()

        ability_name = 'test'
        ability_url = 'test-url'

        with self.assertRaises(AbilitiesNotFoundException):
            storage.get_ability_by_name(ability_name)

        storage.create(ability_name, ability_url)

        ability = storage.get_ability_by_name(ability_name)

        self.assertEquals(ability.name, ability_name)
        self.assertEquals(ability.url, ability_url)

    def test_ability_storage_creating_or_getting(self):
        storage = AbilitiesStorage()

        ability_name = 'test'
        ability_url = 'test-url'

        with self.assertRaises(AbilitiesNotFoundException):
            storage.get_ability_by_name(ability_name)

        ability1 = storage.get_or_create(ability_name, ability_url)
        ability2 = storage.get_or_create(ability_name, ability_url)

        self.assertEquals(ability1.id, ability2.id)
        self.assertEquals(ability1.name, ability2.name)
        self.assertEquals(ability1.url, ability2.url)
