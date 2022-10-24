from projects_provider import ProjectsProvider


class DummyProjectsProvider(ProjectsProvider):

    def __init__(self):
        self._projects = {
            'B': ['A', 'F'],
            'C': ['A'],
            'D': ['B'],
            'E': ['B'],
            'F': ['C'],
            'G': ['C', 'B'],
            'H': []
        }

    def get_projects(self):
        return self._projects
