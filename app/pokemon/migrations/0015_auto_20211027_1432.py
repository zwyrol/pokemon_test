# Generated by Django 3.2.8 on 2021-10-27 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0014_alter_pokemon_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonstats',
            name='id',
        ),
        migrations.AlterField(
            model_name='pokemonstats',
            name='pokemon',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pokemon.pokemon'),
        ),
    ]
