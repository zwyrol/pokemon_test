from app.abilities.models import Ability


class AbilitiesNotFoundException(Exception):
    pass


class AbilitiesStorage:
    def get_ability_by_name(self, name):
        try:
            return Ability.objects.get(name=name)
        except Ability.DoesNotExist:
            raise AbilitiesNotFoundException(f"The ability {name} not found.")

    def create(self, name, url):
        ability = Ability(name=name, url=url)
        ability.save()

        return ability

    def get_or_create(self, name, url):
        try:
            ability = self.get_ability_by_name(name)
        except AbilitiesNotFoundException:
            ability = Ability(name=name, url=url)
            ability.save()

        return ability
