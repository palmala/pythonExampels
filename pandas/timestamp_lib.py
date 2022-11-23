import pandas as pd
from copy import deepcopy


def detect_month_overflows(dataframe: pd.DataFrame, from_column: str = "from", to_column: str = "to") -> set:
    result = set()

    for ind in dataframe.index:
        from_date = pd.Timestamp(dataframe[from_column][ind])
        to_date = pd.Timestamp(dataframe[to_column][ind])
        if from_date.month != to_date.month:
            result.add(tuple([from_date, to_date]))

    return result


def merge_overlaps(dataframe: pd.DataFrame, from_column: str = "from", to_column: str = "to") -> pd.DataFrame:
    result = []
    to_dataframe = _merge_intervals_list(
        [[row[from_column], row[to_column]] for row in dataframe.to_dict('records')])
    for row in to_dataframe:
        result.append({from_column: row[0], to_column: row[1]})

    return pd.DataFrame.from_dict(result)


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


def split_overflows(dataframe: pd.DataFrame, from_column: str = "from", to_column: str = "to") -> pd.DataFrame:
    result = deepcopy(dataframe)
    splits = pd.DataFrame()
    for ind in result.index:
        from_date = pd.Timestamp(result[from_column][ind])
        to_date = pd.Timestamp(result[to_column][ind])
        if from_date.month != to_date.month:
            split_date = to_date.replace(day=1, hour=0, minute=0)
            row = result.iloc[ind].to_dict()
            result.at[ind, to_column] = split_date
            row[from_column] = split_date
            if splits.empty:
                splits = pd.DataFrame.from_dict([row])
            else:
                new_row_df = pd.DataFrame(row)
                splits = pd.concat([splits, new_row_df], ignore_index=True)

    if not splits.empty:
        result = pd.concat([splits, result], ignore_index=True)

    return result
