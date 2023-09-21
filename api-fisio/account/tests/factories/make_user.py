from account.models import User


def make_user(overrides={}):
    user_data = {
        'username': 'test12',
        'email': 'test@gmail.com',
        'password': '123test#',
        'role': 1,
        **overrides
    }

    user = User(**user_data)

    user.save()

    return user
