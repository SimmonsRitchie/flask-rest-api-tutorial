from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):

        # get ItemModel obj from db
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {'message': 'An error occurred finding the store'}, 500 # internal server error

        # return item
        if store:
            return store.json() # using json method in ItemModel to return json
        return {'message':'Store not found'}, 404


    def post(self, name):
        # check if item exists
        if StoreModel.find_by_name(name):
            return {'message':f'A store with name {name} already exists'}, 400 # bad request

        # create StoreModel obj
        store = StoreModel(name)

        # insert store into DB
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500 # internal server error

        # Remember, we can only return JSON so that's why item must be a dict
        return store.json(), 201 # Add '201' created


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}