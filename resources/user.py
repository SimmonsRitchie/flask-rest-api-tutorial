import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    # PARSER
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )

    def post(self):
        # load and parse request
        data = UserRegister.parser.parse_args()

        # check if user already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        # destructuring dict. We know from parser that there will only be two keyword args: username and password
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created succesfully."}, 201
