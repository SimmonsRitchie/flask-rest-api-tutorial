from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # database is at root directory of project, we can change database type here
# Turns off Flask's in-built SQL Alchemy tracker but doesn't turn off flask_sqlalchemy tracker (which is better)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
api = Api(app)

@app.before_first_request
def create_tables():
    # This creates all the tables in our models unless they exist already
    db.create_all()

jwt = JWT(app, authenticate, identity)  # creates /auth endpoint as default, takes user and pass

api.add_resource(Store, '/store/<string:name>') # http://127.0.0.1/store/costco
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/item/juice
api.add_resource(StoreList, '/stores') # http://127.0.0.1/stores
api.add_resource(ItemList, '/items') # http://127.0.0.1/items
api.add_resource(UserRegister, '/register')

# Only the file you run is called '__main__', therefore, we only run our app if we run app.py
# If we imported this file, it wouldn't run app because __name__ of file wouldn't be __main__
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)


"""
JWT CHEAT SHEET

If you may want to configure JWT differently:

Jose blog: https://blog.tecladocode.com/learn-python-advanced-configuration-of-flask-jwt/
FULL DOCS: https://pythonhosted.org/Flask-JWT/

------------------------------------------------------------------------------------------------------
>> Change auth endpoint. Eg /login instead of /auth:

    app.config['JWT_AUTH_URL_RULE'] = '/login'
    jwt = JWT(app, authenticate, identity)
------------------------------------------------------------------------------------------------------

>> Config JWT to expire within half an hour:

    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

------------------------------------------------------------------------------------------------------

>> Config JWT auth key name to be 'email' instead of default 'username'

    app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

------------------------------------------------------------------------------------------------------

>> Sometimes we may want to include more information in the authentication response body, not 
just the access_token. For example, we may also want to include the user's ID in the response body. 
In this case, we can do something like this:

    from flask import jsonify
    from flask_jwt import JWT

    from security import authenticate, identity as identity_function
    jwt = JWT(app, authenticate, identity_function)

    @jwt.auth_response_handler
    def customized_response_handler(access_token, identity):
        return jsonify({
                            'access_token': access_token.decode('utf-8'),
                            'user_id': identity.id
                       })

Remember that the identity should be what you've returned by the authenticate() function, and in our sample, 
it is a UserModel object which contains a field id. Make sure to only access valid fields in your identity model!

Moreover, it is generally not recommended to include information that is encrypted in the access_token since 
it may introduce security issues.

------------------------------------------------------------------------------------------------------

>> By default, Flask-JWT raises JWTError when an error occurs within any of the handlers (e.g. during authentication, 
identity, or creating the response). In some cases we may want to customize what our Flask app does when such an error 
occurs. We can do it this way:

    # customize JWT auth response, include user_id in response body
    from flask import jsonify
    from flask_jwt import JWT
    
    from security import authenticate, identity as identity_function
    jwt = JWT(app, authenticate, identity_function)
    
    @jwt.error_handler
    def customized_error_handler(error):
        return jsonify({
                           'message': error.description,
                           'code': error.status_code
                       }), error.status_code


"""