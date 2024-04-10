from typing import Optional
import random


def get_stuff():
    try:
        result = read_something_from_db()
    except ConnectionError as error:
        result = None
    return result


def read_something_from_db():
    lets_pretend_we_read_something = random.randint(0, 10)
    if lets_pretend_we_read_something >= 5:
        raise ConnectionError("Something went wrong!")
    return lets_pretend_we_read_something


def main():
    my_stuff: int = get_stuff()
    print(my_stuff + 1)


if __name__ == "__main__":
    main()
