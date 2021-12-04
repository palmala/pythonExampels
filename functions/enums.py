from enum import Enum, auto, unique

class Pets(Enum):
    CAT = 1
    DOG = 1

@unique
class UniquePets(Enum):
    CAT = 1
    DOG = 2

class AutoPets(Enum):
    CAT = auto()
    DOG = auto()

if __name__ == "__main__":
    print(Pets.CAT)
    print(type(Pets.CAT))
    print(repr(Pets.CAT))
    print(Pets.CAT.name, Pets.CAT.value)