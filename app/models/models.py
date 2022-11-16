from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

class Tipo(db.Model, BaseModel):
    __tablename__ = 'tipo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'Tipo({self.name})'


class Attack(db.Model, BaseModel):
    __tablename__ = 'attack'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo.id'))
    tipo = db.relationship("Tipo", backref="attacks")


    @classmethod
    def add_attack(cls, attack_name, tipo):
            fill_attack = cls(name = attack_name, tipo = tipo)
            cls.save(fill_attack)

    def __repr__(self):
        return f'Attack({self.name})'

class Pokemon(db.Model, BaseModel):
    __tablename__="pokemon"
    id = db.Column(db.Integer, primary_key=True)
    pokedex_number = db.Column(db.Integer)
    name = db.Column(db.String)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    special = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    tipos = db.relationship("Tipo", uselist= True, secondary="association_table_tipo")
    attacks = db.relationship("Attack", uselist= True, secondary="association_table")


    @classmethod
    def add_pokemon(cls, pokedex_id, pokemon_name, hp, attack, defense, special, speed, tipos):
        fill_pokemon= cls(pokedex_number=pokedex_id, name=pokemon_name, hp=hp, attack=attack, defense=defense, special=special, speed=speed,
                tipos=tipos)
        cls.save(fill_pokemon)

    def __repr__(self):
        return f'Pokemon({self.name})'

class Association(db.Model):
    __tablename__ = "association_table"
    pokemon_id = db.Column(db.ForeignKey("pokemon.id"), primary_key=True)
    ataque_id = db.Column(db.ForeignKey("attack.id"), primary_key=True)

class AssociationTipo(db.Model):
    __tablename__ = "association_table_tipo"
    pokemon_id = db.Column(db.ForeignKey("pokemon.id"), primary_key=True)
    tipo_id = db.Column(db.ForeignKey("tipo.id"), primary_key=True)
