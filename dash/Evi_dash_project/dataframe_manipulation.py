import pandas as pd

def str_to_date_and_sort(df, date_column, date_format=None):		
	if date_format:
		df[date_column] = pd.to_datetime(df[date_column]).dt.strftime(date_format)
	else:
		df[date_column] = pd.to_datetime(df[date_column])
	df.sort_values(by=date_column, inplace=True)


def fill_missing_dates_within_range(df, date_column, frequency, date_format):
	start = min(df[date_column])
	end = max(df[date_column])
	new_date_range_filled = pd.date_range(start=start, end=end, freq=frequency)
	df.set_index(date_column, inplace=True)
	new_index = pd.Index(new_date_range_filled, name=date_column)
	df = df.reindex(new_index, fill_value=0)
	df.reset_index(inplace=True)
	df[date_column] = pd.to_datetime(df[date_column]).dt.strftime(date_format)
	
	return df


def filter_data_between_min_and_max_value(df, column_name, min, max):
	return df.query(f"{column_name} >= {min} and {column_name} <= {max}", inplace=False)


def filter_data_by_column_value(df, column_name, value_for_filtering):
	if value_for_filtering:
		df.query(
			f"{column_name} == '{value_for_filtering}'", inplace=True
		)
		
		
def get_df_with_num_of_items_for_grouped_column_values(df, column_to_groupby, new_column_name_for_numbers):
	return df.groupby(column_to_groupby).size().reset_index(name=new_column_name_for_numbers)


