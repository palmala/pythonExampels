class MyClass:

    def __init__(self, a):
        self._a = a
    
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, new_a):
        if isinstance(new_a, int):
            self._a = new_a
        else:
            raise AttributeError("Attribute 'a' should be int!")
    
    @a.deleter
    def a(self):
        del self._a
    
if __name__ == "__main__":
    my_obj = MyClass(5)
    print(my_obj.a)
    try:
        my_obj.a = 3.14
    except AttributeError as exc:
        print(f'Yep, this is not working: {exc}!')
    my_obj.a = 9
    print(my_obj.a)