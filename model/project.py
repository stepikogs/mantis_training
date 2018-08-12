__author__ = 'George Stepiko'


class Project:
    # limit properties
    # it has id as well
    __slots__ = 'name', \
                'status', \
                'inherit_global', \
                'view_status', \
                'description'

    # constructro with optional arguments
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('decription')
        self.status = kwargs.get('status')
        self.view_status = kwargs.get('view_status')
        self.inherit_global = kwargs.get('inherit_global')

    def __repr__(self):
        return '{}: {}'.format(self.name, self.description)

    def __eq__(self, other):
        return (self.name == other.name) and \
               (self.description == other.description or (self.description is None and other.descrition == ''))
