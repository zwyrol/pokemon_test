# Generated by Django 3.2.8 on 2021-10-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0011_remove_pokemonstats_base_experience'),
        ('abilities', '0002_ability_pokemon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='pokemon',
            field=models.ManyToManyField(related_name='abilities', to='pokemon.Pokemon'),
        ),
    ]
