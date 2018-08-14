__author__ = 'George Stepiko'

import string
import random


def random_user(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    username = random_user('user_', 10)
    password = 'test'
    email = username + '@localhost'
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, password, email)
    assert app.soap.can_login(username, password)

    # in old way:
    # app.session.login(username, password)
    # assert app.session.is_logged_in_as(username)
    # app.session.logout()
