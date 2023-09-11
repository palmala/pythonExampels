from hypothesis import given, assume, note, event, settings, strategies as st
from hypothesis.extra.pandas import column, data_frames, series
from datetime import datetime, timedelta


@given(i=st.integers(0, 10000).filter(lambda x: x % 2 == 0))
@settings(max_examples=20)
def test_example(i):
    assume(i % 10 != 0)
    event(f"Mod 3 event: {i%3}")
    print(i)
    note("If the test fails, this message is printed.")
    assert (i % 2 == 0) and (i % 10 != 0)


@given(i=...)
def test_example2(i: int):
    print(i)


@given(i=st.from_type(int))
def test_example3(i):
    print(i)


@given(...)
@settings(max_examples=15)
def test_example4(a: int, b: str):
    print(a, b)


@given(st.lists(st.integers(), max_size=3))
@settings(max_examples=4)
def test_list(list_arg):
    print(len(list_arg))


def create_diff_from_date_ranges(df):
    df["DIFF"] = df["END"] - df["START"]


df_strategy = data_frames(
    columns=[
        column(
            unique=True,
            name="START",
            elements=st.dates(
                min_value=datetime(2020, 1, 1).date(),
                max_value=datetime(2021, 1, 1).date(),
            ),
        ),
        column(
            unique=True,
            name="END",
            elements=st.dates(
                min_value=datetime(2021, 1, 2).date(),
                max_value=datetime(2022, 1, 1).date(),
            ),
        ),
    ]
)


@given(df=df_strategy)
@settings(max_examples=20)
def test_create_diff_from_date_ranges(df):
    create_diff_from_date_ranges(df)
    print(df)
    if not df.empty:
        assert df["DIFF"].min() >= timedelta(days=1)


@given(s=series(dtype=int))
@settings(max_examples=20)
def test_series(s):
    print(s)


if __name__ == "__main__":
    #   to test with pytest: pytest --hypothesis-show-statistics
    test_example()
    test_list()
    test_create_diff_from_date_ranges()
    test_series()
