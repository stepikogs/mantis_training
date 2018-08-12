__author__ = 'George Stepiko'
import pytest
from fixture.application import Application
import json
import os.path

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture  # (scope='session')
def app(request):
    global fixture
    web_config = load_config(request.config.getoption('--target'))['web']
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    # fixture.session.ensure_login(username=web_config['username'], password=web_config['password'])
    return fixture


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
