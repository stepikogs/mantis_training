__author__ = 'George Stepiko'
from model.project import Project
from random import randrange


def test_add_project(app):
    # preconditions and declarations
    subj = Project(name='testname', decription='Just another description.')
    app.session.login(username='administrator',  # todo add login to fixture (not a part of current task)
                      password='root')
    # as names are unique - provide NO such project in list
    app.project.provide_by_name(name_to_check=subj.name, absence=True)
    old_projects = app.project.get_list()
    # add unique project name
    app.project.create(subj)
    # assertion section
    # straight forward - project is in list now
    assert app.project.name_found(subj.name)
    # list assertion requested
    new_projects = app.project.get_list()
    old_projects.append(subj)
    assert sorted(new_projects, key=lambda p: p.name) == sorted (old_projects, key=lambda p: p.name)
