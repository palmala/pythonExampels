from abc import ABCMeta, abstractmethod

class IPetFactory(metaclass=ABCMeta):

    @abstractmethod
    def get_pet():
        pass

    @abstractmethod
    def get_food():
        pass



class Cat:

    def speak():
        return "Meow!"

    def __str__():
        return "Cat!"


class Dog:

    def speak():
        return "Woof!"

    def __str__():
        return "Dog!"


class DogFactory():

    def get_pet():
        return Dog()

    def get_food():
        return "Dog food"


class CatFactory():

    def get_pet():
        return Cat()

    def get_food():
        return "Cat food"