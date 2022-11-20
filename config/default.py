import os

SECRET_KEY = '123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'

PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///pokemon.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False

ERROR_404_HELP = False

LISTA_TIPO=['bug', 'dragon', 'electric', 'fighting', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal',
                   'poison', 'psychic', 'rock', 'water']

URL_BASE= "https://serebii.net/"

DIRECTORIO = os.path.dirname(os.path.dirname(__file__))

RUTA_SAVE= "/home/marta/PycharmProjects/pokemon/"