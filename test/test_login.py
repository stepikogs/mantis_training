__author__ = 'George Stepiko'


def test_login(app):
        app.session.login(username='administrator',
                          password='root')
        assert app.session.is_logged_in_as('administrator')