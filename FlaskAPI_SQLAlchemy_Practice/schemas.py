from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id= fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True) # load only wh en we are going to receive the data from the client 
    # store = fields.Nested(PlainStoreSchema(), dump_only=True) # it will return the data when it recieve the data from the client 
    # store = fields.Int(required=True)

class StoreSchema(PlainStoreSchema):
    item_id = fields.Nested(PlainItemSchema(), dump_only=True) # it will return the data when it recieve the data from the client 