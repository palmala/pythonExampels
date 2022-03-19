data = []


def register(func):
    print('Registering %s' % func)
    data.append(func)
    return func


@register
def f1():
    print('Running f1()')


def f2():
    print('Running f2()')


def main():
    print('Running main()')
    print('Content of register: ', data)
    f1()
    f2()


if __name__ == '__main__':
    main()
