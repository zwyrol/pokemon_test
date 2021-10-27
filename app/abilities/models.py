from django.db import models
from app.pokemon.models import Pokemon


class Ability(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    pokemon = models.ManyToManyField(Pokemon, related_name='abilities')
