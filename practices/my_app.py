import my_lib
from practices.my_lib import give_me_something
import logging

logging.basicConfig(filename="testreport.log")


if __name__ == "__main__":
    some_value = give_me_something()
    if some_value == "expected":
        logging.info("TestCase1 passed!")
    else:
        logging.info("TestCase1 failed!")
