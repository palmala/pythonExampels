class Example:
    @staticmethod
    def sm(*args):
        return args

    @classmethod
    def cm(*args):
        return args


if __name__ == "__main__":
    print(Example.sm("foo"))
    print(Example.cm("foo"))
