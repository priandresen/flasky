from flask import Blueprint
from flask import request
from app.db import db
from app.models.cat import Cat


cats_bp = Blueprint("cat_bp", __name__, url_prefix="/cats")

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()

    new_cat = Cat(
        name=request_body["name"],
        color=request_body["color"],
        personality=request_body["personality"]
    )

    db.session.add(new_cat)
    db.session.commit()

    response = {
        "id": new_cat.id,
        "name": new_cat.name,
        "color": new_cat.color,
        "personality": new_cat.personality
    }

    return response, 201

@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat).order_by(Cat.id)
    cats = db.session.scalars(query)

    response = []

    for cat in cats:
        response.append({
            "id": cat.id,
            "name": cat.name,
            "color": cat.color,
            "personality": cat.personality
        })

    return response



#create database on postgresql
#initialize objects to represent our database, and migration tools
# --> create new file app/models/base.py
# using this class to establish a base for all of our models to inherit from
# this allows us to map our models to database tables
"""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
    
"""
#--> create a class to represent our Cat model in app/models/cat.py
#register these objects with our application and tell Flask where to find our new database in create_app
#conect app to database

#create db file in app directory
#
""" 
from from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ..models.base import Base

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
"""
#run migrations

#--> modify app/__init__.py to register cat routes in create_app
"""
from flask import Flask
from .db import db, migrate
from .routes.cat_routes import cats_bp

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/flasky_development'


    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(cats_bp)

    return app
    """

#create a model for Cat that inherits from Base
#map Cat model to cats table in the database
#add columns to the cats table that correspond to the attributes of the Cat model

#--> modify app/models/cat.py
"""
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Cat(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    personality: Mapped[str] = mapped_column(nullable=False)
    
"""
#import cat model where needed
#in this case init__.py
#from .models.cat import Cat
#migrations
#run commands in terminal
#flask db init
#flask db migrate -m "Initial migration.// adds cat model"
#flask db upgrade


"""Just like commits, we want to make migrations after each model 
is created or updated because it makes undoing changes a little easier 
if we need to!"""

#create a post request to add new cats to the database
#--> modify app/routes/cat_routes.py
#add a request immport
#from flask import request
#import Cat model from app.models.cat
#from app.models.cat import Cat
#import db from app.db
#from app.db import db

"""
@cats_bp.post("")
def create_cat():
    query = db.select(Cat).order_by(Cat.id)
    cats = db.session.scalars(query)

    request_body = request.get_json()

    new_cat = Cat(
        name=request_body["name"],
        color=request_body["color"],
        personality=request_body["personality"]
    )

    db.session.add(new_cat)
    db.session.commit()

    response = {
        "id": new_cat.id,
        "name": new_cat.name,
        "color": new_cat.color,
        "personality": new_cat.personality
    }

    return response, 201

"""
#get all cats route
"""
@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat).order_by(Cat.id)
    cats = db.session.scalars(query)

    response = []

    for cat in cats:
        response.append({
            "id": cat.id,
            "name": cat.name,
            "color": cat.color,
            "personality": cat.personality
        })

    return response
"""
    