__author__ = 'George Stepiko'
from telnetlib import Telnet


class JamesHelper:

    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, user, pswd):
        james_config = self.app.config['james']
        session = JamesHelper.Session(james_config['host'],
                                      james_config['port'],
                                      james_config['user'],
                                      james_config['pswd'])
        if session.is_user_registered(user):
            session.reset_passwoerd(user, pswd)
        else:
            session.create_user(user, pswd)
        session.quit()

    class Session:

        def __init__(self, host, port, user, pswd):
            self.telnet = Telnet(host=host, port=port, timeout=5)
            self.read_until(match='Login id:', timeout=5)
            self.write(buffer=user + '\n')
            self.read_until(match='Password:', timeout=5)
            self.write(buffer=pswd + '\n')
            self.read_until(match='Welcome %s. HELP for a list of commands' % user, timeout=5)

        def is_user_registered(self, user):
            self.write('verify %s\n' % user)
            res = self.telnet.expect([b'exists', b'does not exist'])
            return res[0] == 0

        def create_user(self, user, pswd):
            self.write('adduser %s %s\n' % (user, pswd))
            self.read_until(match='User %s added' % user, timeout=5)

        def reset_passwoerd(self, user, pswd):
            self.write('setpassword %s %s\n' % (user, pswd))
            self.read_until(match='Password for %s reset' % user, timeout=5)

        def quit(self):
            self.write('quit\n')

        # service
        def read_until(self, match, timeout=5):
            self.telnet.read_until(match.encode('ascii'), timeout=timeout)

        def write(self, buffer):
            self.telnet.write(buffer.encode('ascii'))
