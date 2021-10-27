from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.Pokemon.as_view(), name='pokemons')
]
