import random


def get_my_stuff():
    return str(random.randint(1, 10))


def run():
    stuff = get_my_stuff()
    stuff += 1
    # stuff = 5
    print(stuff)


if __name__ == "__main__":
    run()
