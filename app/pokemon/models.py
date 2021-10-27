from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)


class PokemonStats(models.Model):
    pokemon = models.OneToOneField(Pokemon, on_delete=models.CASCADE, primary_key=True, related_name='stats')
    height = models.IntegerField()
    weight = models.IntegerField()
    base_experience = models.IntegerField()
