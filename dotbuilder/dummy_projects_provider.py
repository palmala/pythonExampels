from projects_provider import ProjectsProvider


class DummyProjectsProvider(ProjectsProvider):

    def __init__(self):
        self._projects = {
            'componentA': ['componentB'],
            'componentC': ['componentB', 'componentA'],
            'componentB': ['componentC']
        }

    def get_projects(self):
        return self._projects
