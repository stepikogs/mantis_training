__author__ = 'George Stepiko'
from model.project import Project
from random import randrange


def test_delete_by_name(app):
    # preconditions and declarations
    remove = Project(name='testname')
    app.session.login(username='administrator',  # todo add login to fixture (not a part of current task)
                      password='root')
    # provide section
    app.project.provide_by_name(remove.name)
    old_projects = app.project.get_list()
    # add
    app.project.delete_by_name(remove.name)
    # assertion section
    # straight forward - project not in list
    assert not app.project.name_found(remove.name)
    # list comparison requested
    new_projects = app.project.get_list()
    for proj in old_projects:
        if proj.name == remove.name:
            old_projects.remove(proj)
    assert sorted(new_projects, key=lambda p: p.name) == sorted (old_projects, key=lambda p: p.name)
