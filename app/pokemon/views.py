from django.shortcuts import render
from django.views.generic.base import View
from app.pokemon.storage import PokemonStorage

class Pokemon(View):
    def get(self, request, *args, **kwargs):
        storage = PokemonStorage()
        return render(request, "pokemons.html", {'pokemons': storage.get_all()})
