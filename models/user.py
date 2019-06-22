from db import db

#NOTE: Model is internal representation of entity, resources are external representations
# Models are essentially helpers without polluting resources.

class UserModel(db.Model):
    __tablename__ = 'users'

    # these must match column names in our database
    id = db.Column(db.Integer, primary_key=True) # autoincrementing, we don't need to create this in __init__
    username = db.Column(db.String(80)) # Good practice to limit sizes
    password = db.Column(db.String(80)) # Good practice to limit sizes

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SELECT * FROM users WHERE username=username


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # # SELECT * FROM users WHERE id=id