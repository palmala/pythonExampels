import pandas
from collections import defaultdict
from copy import deepcopy

import pandas as pd


def detect_month_overflows(dataframe: pandas.DataFrame, from_column: str = "from", to_column: str = "to") -> set:
    result = set()

    for ind in dataframe.index:
        from_date = pandas.Timestamp(dataframe[from_column][ind])
        to_date = pandas.Timestamp(dataframe[to_column][ind])
        if from_date.month != to_date.month:
            result.add(tuple([from_date, to_date]))

    return result


def merge_overlaps(dataframe: pandas.DataFrame, group_by: str = "month", from_column: str = "from",
                   to_column: str = "to") -> pandas.DataFrame:
    grouped = _df_to_dict(dataframe, from_column, to_column, group_by)

    to_dataframe = []
    for key in grouped:
        grouped[key] = _merge_intervals_list(grouped[key])
        for interval in grouped[key]:
            row = {group_by: key, from_column: interval[0], to_column: interval[1]}
            to_dataframe.append(row)

    result = pandas.DataFrame.from_dict(to_dataframe)
    return result


def _df_to_dict(dataframe, from_column, to_column, group_by):
    grouped = defaultdict(list)
    for ind in dataframe.index:
        window = [dataframe[from_column][ind], dataframe[to_column][ind]]
        grouped[dataframe[group_by][ind]].append(window)
    return grouped


def _merge_intervals_list(intervals: list) -> list:
    intervals.sort()
    print(f'intervals: {intervals}')
    result = list()
    result.append(intervals[0])
    for i in intervals[1:]:        
        if result[-1][0] <= i[0] <= result[-1][-1]:
            result[-1][-1] = max(result[-1][-1], i[-1])
        else:
            result.append(i)
    return result


def split_overflows(dataframe: pandas.DataFrame, from_column: str = "from", to_column: str = "to") -> pandas.DataFrame:
    result = deepcopy(dataframe)
    splits = pandas.DataFrame()
    for ind in result.index:
        from_date = pandas.Timestamp(result[from_column][ind])
        to_date = pandas.Timestamp(result[to_column][ind])
        if from_date.month != to_date.month:
            split_date = to_date.replace(day=1, hour=0, minute=0)
            row = result.iloc[ind].to_dict()
            result.at[ind, to_column] = split_date
            row[from_column] = split_date
            if splits.empty:
                splits = pandas.DataFrame.from_dict([row])
            else:
                new_row_df = pd.DataFrame(row)
                splits = pd.concat([splits, new_row_df], ignore_index=True)

    if not splits.empty:
        result = pd.concat([splits, result], ignore_index=True)

    result = result.sort_values([from_column]).reset_index(drop=True)
    return result
