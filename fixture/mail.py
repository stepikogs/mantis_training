__author__ = 'George Stepiko'

import poplib
import email
from time import sleep


class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    msg_lnes = pop.retr(n + 1)[1]
                    msg_text = '\n'.join(map(lambda x: x.decode('utf-8'), msg_lnes))
                    msg = email.message_from_string(msg_text)
                    if msg.get('Subject') == subject:
                        pop.dele(n + 1)
                        pop.quit()
                        return msg.get_payload()
            pop.quit()
            sleep(5)
        return ''
