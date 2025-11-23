from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import ItemModel,StoreModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # raise NotImplementedError("Getting an item is not implemented.")
        item = ItemModel.query.get(item_id)
        if not item:
            abort(404, message="Item not found.")
        return item
        # we can also use instaed of above 
        # item = ItemModel.query.get_or_404(item_id)

    def delete(self, item_id):
        #raise NotImplementedError("Deleting an item is not implemented.")
        item = ItemModel.query.get(item_id)
        if not item:
            abort(404,message="Item not found")
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Deleting an item is not implemented")
        return {"message":"Item is deleted sucessfully"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        #raise NotImplementedError("Updating an item is not implemented.")
        item = ItemModel.query.get(item_id)
        #if item present we are udating te data if it is not htere means we are creating the data on else
        if item:
            item.name = item_data.get("name",item.name)
            item.price = item_data.get("price",item.price)
        else:
            item=ItemModel(id=item_id,**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # raise NotImplementedError("Listing items is not implemented.")
        return ItemModel.query.all()

    @blp.arguments(ItemSchema(many=True))
    @blp.response(201, ItemSchema(many=True))
    def post(self, item_data):
        # store = StoreModel.query.get(item_data.get("store_id"))
        # if not store:
        #     abort(400, message=f"Store with ID {item_data.get('store_id')} does not exist.")

        # item = ItemModel(**item_data)
        created_items = []
        for item_data1 in item_data:
            # Validate store exists
            store = StoreModel.query.get(item_data1.get("store_id"))
            if not store:
                abort(400, message=f"Store with ID {item_data1.get('store_id')} does not exist.")

            item = ItemModel(**item_data1)
            db.session.add(item)
            created_items.append(item)
        try:
            # db.session.add(created_items)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while inserting the item.")

        # return item
        return created_items