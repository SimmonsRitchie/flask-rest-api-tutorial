from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    # we use parser to control what info can be used as args
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                    )

    @jwt_required()
    def get(self, name):

        # get ItemModel obj from db
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred finding the item'}, 500 # internal server error

        # return item
        if item:
            return item.json() # using json method in ItemModel to return json
        return {'message':'Item not found'}, 404


    def post(self, name):
        # check if item exists
        if ItemModel.find_by_name(name):
            return {'message':f'An item with name {name} already exists'}, 400 # bad request

        # load and parse request
        data = Item.parser.parse_args()

        # create ItemModel obj
        item = ItemModel(name, **data) # destructuring data

        # insert item into DB
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500 # internal server error

        # Remember, we can only return JSON so that's why item must be a dict
        return item.json(), 201 # Add '201' created


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}


    def put(self, name):
        # load and parse request
        data = Item.parser.parse_args()

        #determine if item exists
        item = ItemModel.find_by_name(name) # item retrieved from DB

        # create item or edit
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()



class ItemList(Resource):
    def get(self):
        # alternative, lambda version: {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [item.json() for item in ItemModel.query.all()]}
