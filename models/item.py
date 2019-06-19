import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    # these must match column names in our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # Good practice to limit sizes
    price = db.Column(db.Float(precision=2)) # 2 dp

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # connected with stores
    store = db.relationship('StoreModel') # this sees that we have a foreign key, joins automatically

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
            }

    # This remains a class method because it returns an object of type ItemModel
    # rather than a dict.
    @classmethod
    def find_by_name(cls, name):
        # Below is the equivalent of SELECT * FROM items WHERE name=name
        # returns result as ItemModel object
        # .first() equivalent of fetchone().
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # session is a collection of objects to add to the database
        # below is the equivalent of "INSERT INTO items VALUES (?, ?)" and UPDATE
        db.session.add(self)
        # commit adds all the objs from a session to the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
