import re

__author__ = 'George Stepiko'
from selenium import webdriver
from fixture.session import SessionHelper


class Application:

    # fixture methods
    def __init__(self, browser, base_url, db):
        if browser == 'firefox':
            self.wd = webdriver.Firefox(capabilities={"marionette": False})
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError('unrecognized browser %s' % browser)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self, db)
        self.record = RecordHelper(self, db)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            print('fixture is not valid, re-create.')
            return False

    def destroy(self):
        self.wd.quit()
