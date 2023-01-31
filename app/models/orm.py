from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship

from app.models.models import Pokemon, Attack, Tipo

db=SQLAlchemy()
metadata = db.metadata

pokemon = Table("pokemon",
                metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("pokedex_number", Integer),
                Column("name", String),
                Column("hp", Integer),
                Column("attack", Integer),
                Column("defense", Integer),
                Column("special", Integer),
                Column("speed", Integer))

tipos = Table("tipo",
              metadata,
              Column("id", Integer, primary_key=True, autoincrement=True),
              Column("name", String))

attack = Table("attack",
               metadata,
               Column("id", Integer, primary_key=True, autoincrement=True),
               Column("tipo_id", Integer, ForeignKey("tipo.id")),
               Column("name", String))

association_table = Table("association_table",
                          metadata,
                          Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
                          Column("ataque_id", Integer, ForeignKey("attack.id"), primary_key=True))

association_table_tipo = Table("association_table_tipo",
                               metadata,
                               Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
                               Column("tipo_id", Integer, ForeignKey("tipo.id"), primary_key=True))


def start_mappers():
    tipo_mapper = mapper(Tipo, tipos)

    attack_mapper = mapper(Attack, attack, properties={'tipo': relationship(tipo_mapper, backref="attacks")})
    Pokemon_mapper = mapper(Pokemon, pokemon,
                            properties={'tipos': relationship(tipo_mapper, secondary=association_table_tipo, backref='pokemons'),
                                        'attacks': relationship(attack_mapper, secondary=association_table)})
