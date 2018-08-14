__author__ = 'George Stepiko'

from suds.client import Client
from suds import WebFault
from model.project import Project
import re


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

    def get_project_list_by_user(self, username, password):
        client = Client('http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl')
        project_list = []
        raw_list = []
        try:
            raw_list = client.service.mc_projects_get_user_accessible(username, password)
        except WebFault:
            pass
        for record in raw_list:
            project_list.append(self.parse_for_project(record))
        # return raw_list
        return project_list

    # service
    def parse_for_project(self, record):
        extracted = Project()
        # extract name and description as while
        extracted.name = re.search('name = "(.*)"\n', str(record)).group(1)
        descr_raw = re.search('description = (.*)\n', str(record)).group(1)
        if descr_raw == 'None':
            extracted.description = None
        else:
            extracted.description = re.search('"(.*)"', str(descr_raw)).group(1)
        return extracted
