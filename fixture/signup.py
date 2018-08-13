__author__ = 'George Stepiko'

import re


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, user, pswd, email):
        wd = self.app.wd
        wd.get(self.app.base_url + '/signup_page.php')
        self.app.update_text_field('username', user)
        self.app.update_text_field('email', email)
        wd.find_element_by_css_selector('input[type="submit"]').click()

        mail = self.app.mail.get_mail(user, pswd, '[MantisBT] Account registration')
        url = self.extract_confimation_url(mail)

        wd.get(url)
        self.app.update_text_field('password', pswd)
        self.app.update_text_field('password_confirm', pswd)
        wd.find_element_by_css_selector('input[value="Update User"]').click()

    def extract_confimation_url(self, mailtext):
        return re.search("http://.*$", mailtext, re.MULTILINE).group(0)
        # re.search('^http://.*$', mailtext)
