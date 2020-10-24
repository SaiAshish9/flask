from werkzeug.security import safe_str_cmp
from user import User


users=[
User(1,'sai','1234')
]

username_mapping = { u.username: u for u in users }
userId_mapping = { u.id : u for u in users }



def authenticate(username,password):
    # user = username_mapping.get(username, None)
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        # safe way of comparing strings
        return user

def identity(payload):
    user_id = payload['identity']
    # return userId_mapping.get(user_id, None)
    return User.find_by_id(user_id)
