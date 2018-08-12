__author__ = 'George Stepiko'


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username="admin", password="secret"):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector('input[type="submit"]').click()
        # wd.find_element_by_xpath("//form[@id='LoginForm']/input[3]").click()

    def is_logged_in(self):
        wd = self.app.wd
        return wd.find_elements_by_link_text("Logout")

    def is_logged_in_as(self, username):
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector('td.login-info-left span').text
        # return wd.find_element_by_xpath('//div/div[1]/form/b').text[1:-1]

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        if self.is_logged_in():  # len check is not required here
            self.logout()
        else:
            pass

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        else:
            self.login(username=username, password=password)
