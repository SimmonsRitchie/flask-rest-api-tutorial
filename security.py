from werkzeug.security import safe_str_cmp
from models.user import UserModel


# Determines whether username and password match, returns user details that are then turned into JWT token
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password): # safe_str_compare works on all python versions, all servers
        return user

# Invoked when a user accesses an endpoint: Determines if a user's JWT token is valid
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

