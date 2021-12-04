def f(arg1, *, someBoolean=False):
    pass

if __name__ == "__main__":
    try:
        f(1, True)
    except Exception as e:
        print(f"You shouldn't call it like this: {e}")
    f(1, someBoolean=True)