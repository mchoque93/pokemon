from typing import List, Type

from app.api.repositories.abstract_pokemon_repository import AbstractPokemonRepository
from app.models.models import Pokemon, Tipo, Attack
from app.models.orm import db


class MemoryPokemonRepository(AbstractPokemonRepository):

    def get_all_tipos(self):
        return db.session.query(Tipo).all()

    def get_all_pokemons(self):
        return db.session.query(Pokemon).all()

    def get_by_pokedex_numer(self, pokemon_id: int):
        return db.session.query(Pokemon).filter_by(pokedex_number=pokemon_id).first()

    def get_tipo(self, tipo: Type['Tipo'], lista_tipos: List['str']):
        return db.session.query(tipo).filter(tipo.name.in_((lista_tipos))).all()

    def get_pokemon_tipo(self, lista_tipos: List[str]):
        return db.session.query(Pokemon).filter(Pokemon.tipos.any(Tipo.name.in_(lista_tipos))).all()

    def get_by_name(self, name: str):
        return db.session.query(Pokemon).filter_by(name=name).first()

    def add_pokemon(self, pokedex_id, pokemon_name, hp, attack, defense, special, speed, tipos):
        fill_pokemon = Pokemon(pokedex_number=pokedex_id, name=pokemon_name, hp=hp, attack=attack, defense=defense,
                               special=special, speed=speed,
                               tipos=tipos)
        db.session.add(fill_pokemon)
        db.session.commit()

    def add_attack(self, attack_name, tipo):
        fill_attack = Attack(name=attack_name, tipo=tipo)
        db.session.add(fill_attack)
        db.session.commit()

    def add_tipo(self, name_tipo):
        fill_tipo = Tipo(name=name_tipo)
        db.session.add(fill_tipo)
        db.session.commit()
