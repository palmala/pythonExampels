def some_filter(element):
    return element % 2 == 0


if __name__ == "__main__":
    nums = [2, 5, 9, 2, 76, 14, 13, 59, 61, 66, 44]
    print(list(filter(some_filter, nums)))
