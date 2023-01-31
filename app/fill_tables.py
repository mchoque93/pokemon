from app.api.repositories.memory_pokemon_repository import MemoryPokemonRepository
from app.models.models import Tipo, Pokemon
from app.models.services.load_attacks_by_pokemon import load_attacks_by_pokemon
from app.models.services.load_attacks_by_tipo import load_attacks_by_tipo
from app.models.services.load_pokemon_by_tipo import load_pokemon_by_tipo
from config.default import LISTA_TIPO

memory=MemoryPokemonRepository()

def fill_pokemon_tables():
        #load tabla tipos
        for tipo in LISTA_TIPO:
            memory.add_tipo(tipo)

        for tipo in memory.get_all_tipos():
            #tabla ataques -> todos los ataques de un tipo
            load_attacks_by_tipo(tipo)
            #tabla pokemon -> estadísticas y tipo de pokemon
            load_pokemon_by_tipo(tipo)

        #ataques del pokemon
        for pokemon in memory.get_all_pokemons():
            load_attacks_by_pokemon(pokemon)