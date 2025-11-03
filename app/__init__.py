from flask import Flask
from .db import db, migrate
from .models.cat import Cat
from .routes.cat_routes import bp as cats_bp
import os

def create_app(config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(cats_bp)

    return app
 