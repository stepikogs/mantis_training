__author__ = 'George Stepiko'
from model.project import Project


def test_delete_by_name(app):
    # preconditions and declarations
    user = 'administrator'
    pswd = 'root'
    remove = Project(name='testname')
    app.session.login(username=user,  # todo add login to fixture (not a part of current task)
                      password=pswd)
    # provide section
    app.project.provide_by_name(remove.name)
    old_projects = app.soap.get_project_list_by_user(user, pswd)  # get list by soap
    # old_projects = app.project.get_list()  # get list from web
    # add
    app.project.delete_by_name(remove.name)
    # assertion section
    # straight forward - project not in list
    assert not app.project.name_found(remove.name)
    # list comparison requested
    new_projects = app.soap.get_project_list_by_user(user, pswd)  # get list by soap
    # new_projects = app.project.get_list()  # get list from web
    for proj in old_projects:
        if proj.name == remove.name:
            old_projects.remove(proj)
    assert sorted(new_projects, key=lambda p: p.name) == sorted (old_projects, key=lambda p: p.name)
