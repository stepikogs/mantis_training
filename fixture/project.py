__author__ = 'George Stepiko'

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    # projects navigation
    def open_project_manage(self):
        wd = self.app.wd
        # it should be smart
        if wd.current_url.endswith('/manage_proj_page.php') and \
                wd.find_elements_by_xpath("//input[@value='Create New Project']"):
            return
        # go to it if we are not there at the moment
        wd.find_element_by_link_text('Manage').click()
        wd.find_element_by_link_text('Manage Projects').click()

    # creation
    def create(self, project):
        wd = self.app.wd
        self.open_project_manage()
        # go to creation form
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        # fill the creation form opened
        self.fill_form(project)
        # submit form
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        wd.find_element_by_link_text('Proceed').click()
        self.project_cash = None

    def delete_by_name(self, pray_name):
        wd = self.app.wd
        self.open_project_manage()
        # go to project to delete
        wd.find_element_by_link_text(pray_name).click()
        # initiate deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # confirm deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # we are on project manage after another project is deleted
        # reset cash
        self.project_cash = None

    # load
    project_cash = None

    def get_list(self):
        wd = self.app.wd
        self.open_project_manage()
        project_cache = []
        for row in wd.find_elements_by_css_selector("table.width100 tr[class='row-1']") +\
                    wd.find_elements_by_css_selector("table.width100 tr[class='row-2']"):
            name = row.find_elements_by_css_selector("td")[0].text
            description = row.find_elements_by_css_selector("td")[4].text
            # cells = row.find_elements_by_css_selector("td")
            # name = cells[0].text
            project_cache.append(Project(name=name,
                                         decription=description))
        return list(project_cache)

    # service
    def fill_form(self, donor):
        self.app.update_text_field(field='name', value=donor.name)
        self.app.update_text_field(field='description', value=donor.description)

    def name_found(self, name_to_check):
        wd = self.app.wd
        return wd.find_elements_by_link_text(name_to_check)

    def provide_by_name(self, name_to_check, absence=False):
        # go to project manage if required (smart)
        self.open_project_manage()
        # check name
        if not self.name_found(name_to_check) and absence is False:
            self.create(Project(name=name_to_check))
        elif self.name_found(name_to_check) and absence is True:
            self.delete_by_name(name_to_check)

