from functools import wraps


def wrapper_with_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Wrapper can now do something with {args} and {kwargs}')
        print(f'Starting actual function')
        result = func(*args, **kwargs)
        print(f'Leaving wrapper')
        return result

    return wrapper


@wrapper_with_arguments
def f(*args, **kwargs):
    print(f'args: {args}')
    print(f'kwargs: {kwargs}')


if __name__ == "__main__":
    f()
    f(1, 2, 3)
    f(a=1, b=2)
    f(1, 2, a=3, b=4)
