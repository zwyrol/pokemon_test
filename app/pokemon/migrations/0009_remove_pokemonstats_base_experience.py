# Generated by Django 3.2.8 on 2021-10-27 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0008_pokemonstats_base_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonstats',
            name='base_experience',
        ),
    ]