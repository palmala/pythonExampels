from functools import wraps


def separators(f):
    @wraps(f)
    def wrapper():
        print("-----")
        f()
        print("-----")

    return wrapper


def more_separators(f): 
    @wraps(f)
    def wrapper():
        print("=====")
        f()
        print("=====")

    return wrapper


@more_separators
@separators
def func1():
    print("Hello!")


if __name__ == "__main__":
    func1()
