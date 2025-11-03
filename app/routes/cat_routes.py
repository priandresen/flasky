from flask import Blueprint, make_response, abort, Response
from flask import request
from app.db import db
from app.models.cat import Cat


cats_bp = Blueprint("cat_bp", __name__, url_prefix="/cats")



def validate_cat(id):
    try:
        id = int(id)
    except ValueError:
            invalid = {"message": f"Cat {id} is invalid. Must be an integer"}
            abort(make_response(invalid, 400))

    query = db.select(Cat).where(Cat.id == id)
    cat = db.session.get(Cat, id)

    if not cat:
        not_found = {"message": f"Cat with id {id} not found"}
        abort(make_response(not_found, 404))

    return cat

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()

    new_cat = Cat.from_dict(request_body)

    db.session.add(new_cat)
    db.session.commit()

    return new_cat.to_dict(), 201

@cats_bp.get("")
def get_all_cats():

    name_param = request.args.get("name") #example of getting a query parameter, not used here
    #what is request.args? it's a dictionary-like object that contains all the query parameters in the URL
    #where is it? in the request object imported from flask
    #how do you access it? request.args.get("name")
    color_param = request.args.get("color")
    personality_param = request.args.get("personality")

    query = db.select(Cat)

    #find out if a name query parameter was provided
    if name_param:
        #explain query arg by arg: 
        # query = db.select(Cat)  --> select all columns from Cat table
        #.where(Cat.name == name_param) --> filter the results where the name column matches the name_param value
        #.order_by(Cat.id) --> order the results by the id column
        query = query.where(Cat.name == name_param).order_by(Cat.id)
    #if not, get all cats
    if color_param:
        query = query.where(Cat.color.ilike(f"%{color_param}%")).order_by(Cat.id)
    if personality_param:
        query = query.where(Cat.personality.ilike(f"%{personality_param}%")).order_by(Cat.id)
    else:
        #build the query to get all cats ordered by their id
        query = query.order_by(Cat.id)

    #execute the query and get the results
    cats = db.session.scalars(query)

    response = []

    for cat in cats:
        response.append(cat.to_dict())

    return response

@cats_bp.get("/<id>")
def get_single_cat(id):

    cat = validate_cat(id) 

    return cat.to_dict()

@cats_bp.put("/<id>")
def replace_cat(id):
    cat = validate_cat(id)

    request_body = request.get_json()

    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]

    #saves to the database
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@cats_bp.delete("/<id>")
def delete_cat(id):
    cat = validate_cat(id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

    #build the query to get a cat by its id
    # query = db.select(Cat).where(Cat.id == id)
    # #execute the query and get the result
    # cat = db.session.scalar(query)
    #if it doesn't exist, this returns None