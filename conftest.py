__author__ = 'George Stepiko'
import pytest
from fixture.application import Application
import json
import jsonpickle
import os.path
import importlib
from fixture.db import DbFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(request.config.getoption('--target'))['db']
    dbfixture = DbFixture(host=db_config['host'],
                          name=db_config['name'],
                          user=db_config['user'],
                          password=db_config['password'])

    def finik():
        dbfixture.destroy()
    request.addfinalizer(finik)
    return dbfixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):

    def finik():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(finik)
    return fixture


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')
    parser.addoption('--target', action='store', default='target.json')
