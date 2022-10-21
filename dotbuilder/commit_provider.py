from abc import ABC, abstractmethod


class CommitProvider(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_number_of_commits(self, component):
        pass

