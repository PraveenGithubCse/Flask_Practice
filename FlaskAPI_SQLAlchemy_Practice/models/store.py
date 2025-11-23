from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic",cascade="all, delete")#same as mentioned in the items.py and for the lazy=dynamic--> it is won't fetch the item detials unitil we tell i.e the condion maches as id got to be equal.. cascade-->> wil delete the items assciated with the store id  will be going to delete