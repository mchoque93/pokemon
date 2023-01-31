import os

from apiflask import APIFlask
from app.api.resources import pokemon_v1_0_bp
from app.fill_tables import fill_pokemon_tables
from app.models.models import Pokemon
from app.models.ext import ma, migrate
from app.models.orm import start_mappers, db


def create_app():
    settings_module = os.getenv('APP_SETTINGS_MODULE')
    app = APIFlask(__name__)
    app.config.from_object(settings_module)

    # Inicializa las extensiones
    with app.app_context():
        db.init_app(app)
        start_mappers()
        db.drop_all()
        db.create_all()

        if db.session.query(Pokemon).first() is None:
            #fill tables
            fill_pokemon_tables()

    migrate.init_app(app, db)
    ma.init_app(app)

    # Captura todos los errores 404
    #Api(app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    #app.url_map.strict_slashes = False

    # Registra los blueprints
    app.register_blueprint(pokemon_v1_0_bp)

    # Registra manejadores de errores personalizados
    #register_error_handlers(app)



    return app