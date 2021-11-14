import random
import itertools


def some_filter_function(x):
    if x < 50:
        return True
    else:
        return False


def get_number():
    return random.randint(0, 10)

if __name__ == "__main__":
    # iterate and stop at a certain element
    for num in iter(get_number, 5):
        print(num)

    # shifting index
    numbers = ["one", "two", "three", "four"]
    for index, value in enumerate(numbers, start=1):
        print(index, value)

    # chaining iterables
    print(list(itertools.chain("ASDASD", range(5))))

    #takewhile, dropwhile
    elements = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 20, 30, 40]
    print(list(itertools.dropwhile(some_filter_function, elements)))
    print(list(itertools.takewhile(some_filter_function, elements)))
