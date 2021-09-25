from user import User

def authenticate(username, password):
    # Looks for username, returns None if not found
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
