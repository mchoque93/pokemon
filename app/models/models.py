from dataclasses import dataclass, field
from typing import List

from flask_sqlalchemy import SQLAlchemy


@dataclass
class Tipo:
    id: int = field(init=False)
    name: str
    attacks: List["Attack"] = field(default_factory=list)
    pokemons: List["Pokemon"] = field(default_factory=list)

    def __repr__(self):
        return f'Tipo({self.name})'


@dataclass
class Attack:
    id: int = field(init=False)
    name: str
    tipo: "Tipo"

    def __repr__(self):
        return f'Attack({self.name})'


@dataclass
class Pokemon:
    id: int = field(init=False)
    pokedex_number: int
    name: str
    hp: int
    attack: int
    defense: int
    special: int
    speed: int
    tipos: List["Tipo"] = field(default_factory=list)
    attacks: List["Attack"] = field(default_factory=list)

    def __repr__(self):
        return f'Pokemon({self.name})'
