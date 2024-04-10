from typing import TypeAlias, NewType

Vector: TypeAlias = list[float]


def foo(param: Vector) -> Vector:
    return [2.3 * x for x in param]


def main():
    foo([1.5, 2.0])


if __name__ == "__main__":
    main()