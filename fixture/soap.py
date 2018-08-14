__author__ = 'George Stepiko'

from suds.client import Client
from suds import WebFault

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, user, pswd):
        client = Client('http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_login(user, pswd)
            return True
        except WebFault:
            return False
