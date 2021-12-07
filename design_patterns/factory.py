class Pet:

    def __init__(self, name):
        self.name = name
        self.sound = "Kwak!"

    def speak(self):
        return self.sound


class Cat(Pet):

    def __init__(self, name):
        super().__init__(name)
        self.sound = "Meow!"


class Dog(Pet):

    def __init__(self, name):
        super().__init__(name)
        self.sound = "Woof!"


def pet_factory(pet="cat"):

    pets = dict(cat=Cat("Muci"),dog=Dog("Lafayette"))
    return pets[pet]

my_cat = pet_factory()
my_dog = pet_factory("dog")
print(my_cat, my_dog)