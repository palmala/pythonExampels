from abc import ABC, abstractmethod


class ProjectsProvider(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_projects(self):
        pass
