# Generated by Django 3.2.8 on 2021-10-27 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_auto_20211027_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonabilities',
            name='pokemon',
        ),
        migrations.AddField(
            model_name='pokemonabilities',
            name='pokemon',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pokemon.pokemon'),
            preserve_default=False,
        ),
    ]