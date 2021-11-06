import secrets
import random
import uuid
import statistics

if __name__ == "__main__":
    # pick random elements from a list
    pieces = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
    weights = [8, 2, 2, 2, 1, 1]
    print(random.choices(pieces, weights, k=10))

    # generate random ids
    id = uuid.uuid4()
    print("UUID4 generated:", uuid.uuid4())
    print("UUID4 hex:", id.hex)
    print("UUID4 urn:", id.urn)

    # statistics
    elements = [2, 3, 5, 7, 11, 13, 17, 19, 3, 5, 2, 7, 5, 3 , 2, 2]
    print(f'Mean is {statistics.mean(elements)}')
    print(f'Median is {statistics.median(elements)}')
    print(f'Median low is {statistics.median_low(elements)}')
    print(f'Median high is {statistics.median_high(elements)}')

    print(f'Most frequent element is {statistics.mode(elements)}')
    print(f'Mean is {statistics.mean(elements)}')
    print(f'Standard deviation is {statistics.stdev(elements)}')


