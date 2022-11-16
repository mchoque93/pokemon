from typing import List

from app.api.repositories.abstract_pokemon_repository import AbstractPokemonRepository
from app.models.models import db, Pokemon, Tipo


class MemoryPokemonRepository(AbstractPokemonRepository):

    def get_all(self, tipo: 'Tipo'):
        return db.session.query(tipo).all()

    def get_by_pokedex_numer(self, pokemon_id: int):
        return db.session.query(Pokemon).filter_by(pokedex_number= pokemon_id).first()

    def get_tipo(self, tipo: 'Tipo', lista_tipos: List['str']):
        return db.session.query(tipo).filter(tipo.name.in_((lista_tipos))).all()

    def get_pokemon_tipo(self, lista_tipos: List[str]):
        return db.session.query(Pokemon).filter(Pokemon.tipos.any(Tipo.name.in_(lista_tipos))).all()

    def get_by_name(self, name: str):
        return db.session.query(Pokemon).filter_by(name= name).first()
