from abc import ABC, abstractmethod


class Checker(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check(self, row: dict) -> dict:
        pass
