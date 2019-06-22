from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    # these must match column names in our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)) # Good practice to limit sizes
    # Below, this says: 'we have a relationship with ItemModel'
    # It then looks at ItemModel and sees that each store has a one-to-many relationship with the items
    # lazy=dynamic, only looks into table when we access the data (eg. using json method.)
    # Pro: Faster to create table, Con: Takes longer when we access data, like using 'json' method
    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
            }

    @classmethod
    def find_by_name(cls, name):
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
