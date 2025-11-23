from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema, ItemSchema


blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        #raise NotImplementedError("Getting a store is not implemented.")
        store = StoreModel.query.get(store_id)
        if not store:
            abort(404, message="Store not found.")
        return store

    def delete(self, store_id):
        #raise NotImplementedError("Deleting a store is not implemented.")
        store = StoreModel.query.get(store_id)
        if not store:
            abort(404,message="Store not found")
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Deleting an Store is not implemented")
        return {"message":"Store is deleted sucessfully"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        #raise NotImplementedError("Listing stores is not implemented.")
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store