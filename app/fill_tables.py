from app.models.models import Tipo, Pokemon
from app.models.services.load_attacks_by_pokemon import load_attacks_by_pokemon
from app.models.services.load_attacks_by_tipo import load_attacks_by_tipo
from app.models.services.load_pokemon_by_tipo import load_pokemon_by_tipo
from config.default import LISTA_TIPO


def fill_pokemon_tables():
        #load tabla tipos
        for tipo in LISTA_TIPO:
            fill_tipo = Tipo(name=tipo)
            fill_tipo.save()

        for tipo in Tipo.query.all():
            #tabla ataques -> todos los ataques de un tipo
            load_attacks_by_tipo(tipo)
            #tabla pokemon -> estadísticas y tipo de pokemon
            load_pokemon_by_tipo(tipo)

        #ataques del pokemon
        for pokemon in Pokemon.query.all():
            load_attacks_by_pokemon(pokemon)