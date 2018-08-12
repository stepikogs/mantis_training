import re

__author__ = 'George Stepiko'
from selenium import webdriver
from fixture.session import SessionHelper


class Application:

    # fixture methods
    def __init__(self, browser, base_url):
        if browser == 'firefox':
            self.wd = webdriver.Firefox(capabilities={"marionette": False})
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError('unrecognized browser %s' % browser)
        self.session = SessionHelper(self)
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

    # common methods
    def open_home_page(self):
        wd = self.wd
        # if wd.current_url.endswith('/addressbook/') and wd.find_elements_by_xpath('//img[@title="Details"]'):
        #     return
        wd.get(self.base_url)

    def return_to_home_page(self):
        wd = self.wd
        wd.find_element_by_link_text("home").click()

    def select_first(self):
        self.select_by_index(0)

    def select_by_index(self, index):
        wd = self.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_by_id(self, id):
        wd = self.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def update_text_field(self, field, value):
        """
        updates field with value
        field if assumed to be text and exists

        :param field:
        :param value:
        :return:
        """
        wd = self.wd
        if value:  # is not None:
            wd.find_element_by_name(field).click()
            wd.find_element_by_name(field).clear()
            wd.find_element_by_name(field).send_keys(value)
            # print(field + ' property is set as "' + str(value) + '".')  # str(value) as value could be INT for years
        else:
            # print(field + ' property has been PASSED as None (check: ' + str(value) + ').')  # debug print
            pass

    def read_text_field(self, field):
        wd = self.wd
        # find the field and return its value (field is assumed to be present, no additional checks requested here)
        return wd.find_element_by_name(field).get_attribute('value')

    def upload_file(self, field, path):
        """
        uploads file in easy way

        :param field: button to submit a file
        :param path: absolute path to file
        :return:
        """
        wd = self.wd
        if path:
            wd.find_element_by_name(field).send_keys(path)
        else:
            # print('Nothing to upload')
            pass

    @staticmethod
    def htmlize_it(raw_string):
        # html replaces multiple spaces with the only space
        # traveling spaces are ignored as well
        return re.sub('\s{2,}', ' ', raw_string.strip())
