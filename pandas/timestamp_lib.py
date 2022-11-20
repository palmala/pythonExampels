import pandas
from collections import defaultdict


def detect_month_overflows(dataframe: pandas.DataFrame, from_column: str = "from", to_column: str = "to") -> set:
    result = set()

    for idx, row in dataframe.iterrows():
        from_date = pandas.Timestamp(row[from_column])
        to_date = pandas.Timestamp(row[to_column])
        if from_date.month != to_date.month:
            result.add(tuple([from_date, to_date]))

    return result


def merge_overlaps(dataframe: pandas.DataFrame, group_by: str = "month", from_column: str = "from",
                   to_column: str = "to") -> pandas.DataFrame:
    grouped = defaultdict(list)

    for ind in dataframe.index:
        window = [dataframe[from_column][ind], dataframe[to_column][ind]]
        grouped[dataframe[group_by][ind]].append(window)

    to_dataframe = []
    for key in grouped:
        grouped[key] = _merge_intervals_list(grouped[key])
        for interval in grouped[key]:
            row = {group_by: key, from_column: interval[0], to_column: interval[1]}
            to_dataframe.append(row)

    result = pandas.DataFrame.from_dict(to_dataframe)
    return result


def _merge_intervals_list(intervals: list) -> list:
    intervals.sort()
    result = list()
    result.append(intervals[0])
    for i in intervals[1:]:
        if result[-1][0] <= i[0] <= result[-1][-1]:
            result[-1][-1] = max(result[-1][-1], i[-1])
        else:
            result.append(i)
    return result
