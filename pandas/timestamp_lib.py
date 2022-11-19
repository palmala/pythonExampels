import pandas


def detect_month_overflows(dataframe: pandas.DataFrame, from_column: str = "from", to_column: str = "to") -> set:
    result = set()

    for idx, row in dataframe.iterrows():
        from_date = pandas.Timestamp(row[from_column])
        to_date = pandas.Timestamp(row[to_column])
        if from_date.month != to_date.month:
            result.add(tuple([from_date, to_date]))

    return result
