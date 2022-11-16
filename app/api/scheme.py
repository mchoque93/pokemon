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