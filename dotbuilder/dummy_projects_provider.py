from projects_provider import ProjectsProvider


class DummyProjectsProvider(ProjectsProvider):

    def __init__(self):
        self._projects = {
            'B': ['A', 'F'],
            'C': ['A'],
            'D': ['B', 'F'],
            'E': ['B'],
            'F': ['C', 'G'],
            'G': ['C'],
            'A': ['F']
        }

    def get_projects(self):
        return self._projects
