import os

from apiflask import APIBlueprint
from flask import request, Blueprint
from flask_restful import Api, Resource

from app.api.repositories.memory_pokemon_repository import MemoryPokemonRepository
from app.api.repositories.tabla_tipos import EquivalenciaDebilidad, initialize_equivalence_dictionary
from app.models.models import Tipo, Pokemon
from app.api.scheme import TipoSchema, Tipos, PokemonSchema, PokemonRecommendadorSchema
from app.models.recommendador.recommendador import Recomendador, load_csv_pokemon
from config.default import DIRECTORIO

pokemon_v1_0_bp = APIBlueprint('pokemon_v1_0_bp', __name__, url_prefix='/pokemon')


tipo_schema = TipoSchema()
pokemon_schema = PokemonSchema()
recomendacion_schema = PokemonRecommendadorSchema()

memory=MemoryPokemonRepository()

equivalencia = EquivalenciaDebilidad(initialize_equivalence_dictionary(os.path.join(DIRECTORIO, 'TIPOS_2.csv')))

@pokemon_v1_0_bp.get("/")
@pokemon_v1_0_bp.output(schema=TipoSchema(many=True))
def get():
    """
    Tipos pokemon
    :return:
    """
    tipo = memory.get_all(Tipo)
    result = tipo_schema.dump(tipo, many=True)
    return result

@pokemon_v1_0_bp.get("/<int:pokemon_id>/counter")
@pokemon_v1_0_bp.output(schema=TipoSchema(many=True))
def stronger_types_of_pokemon(pokemon_id: int):
    """
    Tipos más fuertes contra el pokemon
    :return:
    """
    pokemon = memory.get_by_pokedex_numer(pokemon_id)
    tipos_mas_fuertes = equivalencia.calculate_debilidad(pokemon, equivalencia.diccionario)
    tipos=memory.get_tipo(Tipo, tipos_mas_fuertes)
    result = tipo_schema.dump(tipos, many=True)
    return result

@pokemon_v1_0_bp.post("<string:tipos>/pokemon_counter")
@pokemon_v1_0_bp.output(schema=PokemonSchema(many=True))
def pokemon_types(tipos):
    """
    Pokemons de los tipos introducidos
    :return:
    """
    lista_tipos=[tipo.strip() for tipo in tipos.split(",")]
    pokemons=memory.get_pokemon_tipo(lista_tipos)
    result = pokemon_schema.dump(pokemons, many=True)
    return result

@pokemon_v1_0_bp.post("<string:name>/best_pokemons")
@pokemon_v1_0_bp.output(schema=PokemonSchema(many=True))
def stronger_pokemons_againts_pokemon(name):
    """
    Pokemons más fuertes contra el pokemon introducido
    :return:
    """
    pokemon = memory.get_by_name(name)
    pokemon_tipos_mas_fuertes = equivalencia.calculate_debilidad(pokemon, equivalencia.diccionario)
    pokemons = memory.get_pokemon_tipo(pokemon_tipos_mas_fuertes)
    result = pokemon_schema.dump(pokemons, many=True)
    return result

@pokemon_v1_0_bp.get("<int:pokedex_id>/recommend")
@pokemon_v1_0_bp.output(schema=PokemonRecommendadorSchema(many=True))
def recommendador(pokedex_id):
    """
    Recomendador pokemons similares
    :return:
    """
    recomendador = Recomendador(load_csv_pokemon())
    recomendaciones = recomendador.recommend(pokedex_id)
    result = recomendacion_schema.dump(recomendaciones, many=True)
    return result