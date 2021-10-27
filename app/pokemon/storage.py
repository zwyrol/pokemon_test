from app.pokemon.models import Pokemon, PokemonStats


class PokemonNotFoundException(Exception):
    pass


class PokemonStatsNotFoundException(Exception):
    pass


class PokemonStorage:
    def get_all(self):
        return Pokemon.objects.all()

    def get_pokemon_by_name(self, name):
        try:
            return Pokemon.objects.get(name=name)
        except Pokemon.DoesNotExist:
            raise PokemonNotFoundException(f"The pokemon {name} not found.")

    def create(self, name, url):
        pokemon = Pokemon(name=name, url=url)
        pokemon.save()

        return pokemon

    def get_or_create(self, name, url):
        try:
            pokemon = self.get_pokemon_by_name(name)
        except PokemonNotFoundException:
            pokemon = self.create(name, url)

        return pokemon


class PokemonAbilityStorage:
    def get_by_pokemon(self, pokemon):
        return list(pokemon.abilities.all())

    def create(self, pokemon, ability):
        pokemon.abilities.add(ability)

        return pokemon.abilities.all()

    def remove_all(self, pokemon):
        pokemon.abilities.clear()


class PokemonStatsStorage:
    def get_by_pokemon(self, pokemon):
        try:
            return PokemonStats.objects.get(pokemon=pokemon)
        except PokemonStats.DoesNotExist:
            raise PokemonStatsNotFoundException(f"The pokemon stats for {pokemon.name} not found.")

    def create(self, pokemon, height, weight, base_experience):
        stats = PokemonStats(pokemon=pokemon, height=height, weight=weight, base_experience=base_experience)
        stats.save()

        return stats

    def remove(self, pokemon):
        try:
            PokemonStats.objects.get(pokemon=pokemon).delete()
        except PokemonStats.DoesNotExist:
            return False

        return True
