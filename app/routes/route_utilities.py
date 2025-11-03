from flask import abort, make_response
from app.db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
            invalid = {"message": f"{cls.__name__} id {model_id} is invalid. Must be an integer"}
            abort(make_response(invalid, 400))

        #what is query doing here? It is creating a SQL query to select a record from the database table corresponding to the class 'cls' where the id matches 'model_id'.
    query = db.select(cls).where(cls.id == model_id)
    #what is model doing here? It is executing the query created above and retrieving a single record from the database that matches the criteria.
    model = db.session.scalar(query)

    if not model:
        not_found = {"message": f"{cls.__name__} with id {model_id} not found"}
        abort(make_response(not_found, 404))

    return model