from marshmallow import fields

from app.models.ext import ma

class TipoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=False)

class Tipos(ma.Schema):
    name = fields.String(required=False)

class PokemonSchema(ma.Schema):
    name = fields.String(required=False)
    tipos = fields.String(required=False, many=True)


class PokemonRecommendadorSchema(ma.Schema):
    pokemon_id = fields.Integer(required=False)
    pokemon_id = fields.Integer(required=False)
    name = fields.String(required=False)
    hp = fields.Integer(required=False)
    attack = fields.Integer(required=False)
    defense = fields.Integer(required=False)
    special = fields.Integer(required=False)
    speed = fields.Integer(required=False)
    tipos = fields.String(required=False, many=True)
