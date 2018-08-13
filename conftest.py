__author__ = 'George Stepiko'
import pytest
from fixture.application import Application
import json
import os.path
import ftputil

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
def config(request):
    return load_config(request.config.getoption('--target'))


@pytest.fixture  # (scope='session')
def app(request, config):
    global fixture
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # fixture.session.ensure_login(username=web_config['username'], password=web_config['password'])
    return fixture


@pytest.fixture(scope='session', autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'],
                                 config['ftp']['username'],
                                 config['ftp']['password'])

    def finik():
        restore_server_configuration(config['ftp']['host'],
                                     config['ftp']['username'],
                                     config['ftp']['password'])
    request.addfinalizer(finik)


def install_server_configuration(host, user, pswd):
    with ftputil.FTPHost(host, user, pswd) as remote:
        if remote.path.isfile('config_inc.php.bk'):
            remote.remove('config_inc.php.bk')
        if remote.path.isfile('config_inc.php'):
            remote.rename('config_inc.php', 'config_inc.php.bk')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resources/config_inc.php'), 'config_inc.php')


def restore_server_configuration(host, user, pswd):
    with ftputil.FTPHost(host, user, pswd) as remote:
        if remote.path.isfile('config_inc.php.bk'):
            if remote.path.isfile('config_inc.php'):
                remote.remove('config_inc.php')
            remote.rename('config_inc.php.bk', 'config_inc.php')

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
