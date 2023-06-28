#!/usr/bin/env python3

import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dataframe_manipulation import str_to_date_and_sort, fill_missing_dates_within_range, filter_data_between_min_and_max_value, filter_data_by_column_value, get_df_with_num_of_items_for_grouped_column_values
									


CSV = "incidents2.csv"

df = pd.read_csv(CSV)
str_to_date_and_sort(df, 'DATE')
df["LIKES"] = df["LIKES"].astype(int)
countries = df["COUNTRY"].sort_values().unique()
chart_types = ['line', 'bar']
country_dropdown_options = [{"label": country, "value": country} for country in countries]
country_dropdown_options.append({"label": "ALL", "value": ""})

app = Dash(__name__)

app.title = "Evi project"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Incident Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze the number of incidents"
                        " amongst different countries between 2021 and 2022"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=country_dropdown_options,
                            value="ENG",
							clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
				html.Div(
					children=[
						html.Div(children="Chart Type", className="menu-title"),
						dcc.Dropdown(
							id="type-filter",
							options=[
								{
									"label": chart_type,
									"value": chart_type,
								}
								for chart_type in chart_types
							],
							value="line",
							clearable=False,
							searchable=False,
							className="dropdown",
						),
					],
				),
				html.Div(
					[
						dmc.Checkbox(id="moving-average", label="Show moving average", mb=10),
					]
				)

				
			],
            className="menu",
        ),
        html.Div(
            children=[
				html.Div([
					dcc.RangeSlider(10, 300, 50, value=[10, 300], id='my-range-slider'),
					html.Div(id='output-container-range-slider')
				], style={'width':'49%', 'background':'gray'}),
				html.Div(
					[
						dbc.Card([
							dbc.CardHeader(""),
							dbc.CardBody(
								html.Div(
									children=dcc.Graph(
										id="incidents-chart",
										config={"displayModeBar": False},
									),
									className="card",
								)
								
							),
							dbc.Container([
								dbc.Label('Data in table'),
								dash_table.DataTable(id='datatable'),
							]),
						]
						)
					]
				)
			],
            className="wrapper",
        ),
    ]
)



def create_data_list_for_chart(df, x, y, charttype):
	return [
		{
			"x": df[x],
			"y": df[y],
			"type": charttype,
		}
	]


def add_moving_average_date_to_data_list(df, x, y, column_to_have_moving_avg, data_list):
	df[y] = df[column_to_have_moving_avg].rolling(3).mean()
	data_list.append({
		"x": df[x],
		"y": df[y],
		"type": "line",
		'line': {'color':'red'}
	})


def create_chart_figure(data_list, chart_name):
	return {
		"data": data_list,
		"layout": {
			"title": {
				"text": chart_name,
				"x": 0.05,
				"xanchor": "left",
			},
			"xaxis": {"fixedrange": True},
			"colorway": ["#17B897"],
		},
	}
	
	
@app.callback(
    Output("incidents-chart", "figure"),
    Output("datatable", "data"),
	Output('output-container-range-slider', 'children'),
	Input("region-filter", "value"),
	Input("type-filter", "value"),
	Input("moving-average", "checked"),
	Input('my-range-slider', 'value')
)
def update_charts(country, charttype, moving_avg_checked, range_selector_value):
	min_value_of_likes = range_selector_value[0]
	max_value_of_likes = range_selector_value[1]
	filtered_data = filter_data_between_min_and_max_value(df, 'LIKES', min_value_of_likes, max_value_of_likes)
	filter_data_by_column_value(filtered_data, 'COUNTRY', country)
	gb_filtered_data = get_df_with_num_of_items_for_grouped_column_values(filtered_data, 'DATE', 'num_of_incidents')
	str_to_date_and_sort(gb_filtered_data, 'DATE')
	gb_filtered_data = fill_missing_dates_within_range(gb_filtered_data, 'DATE', 'MS', '%Y-%m')
	data_list = create_data_list_for_chart(gb_filtered_data, 'DATE', 'num_of_incidents', charttype)
	if moving_avg_checked:
		add_moving_average_date_to_data_list(gb_filtered_data, 'DATE', 'moving_average', 'num_of_incidents', data_list)
	incidents_chart_figure = create_chart_figure(data_list, f'Number of incidents in {country}')
	
	filtered_data = filtered_data[['DATE', 'COUNTRY', 'INCIDENT_ID', 'LIKES']]
	str_to_date_and_sort(filtered_data, 'DATE', '%Y-%m')	
	datatable = filtered_data.to_dict(orient='records')
	selector_str = f"Filtered likes data from {min_value_of_likes} to {max_value_of_likes}"
	
	return incidents_chart_figure, datatable, selector_str


if __name__ == "__main__":
    app.run_server(debug=True)
	