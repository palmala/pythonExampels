#!/usr/bin/env python3

import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

def cast_date_str_to_date_and_sort(df):
	df['DATE'] = pd.to_datetime(df['DATE'])
	df.sort_values(by='DATE', inplace=True)
	new_date_range_filled = pd.date_range(start='2021-01-01', end='2023-01-01', freq='MS')
	df.set_index("DATE", inplace=True)
	new_index = pd.Index(new_date_range_filled, name="DATE")
	df = df.reindex(new_index, fill_value=0)
	df.reset_index(inplace=True)
	df['DATE'] = pd.to_datetime(df['DATE']).dt.strftime('%Y-%m')
	
	return df

data = (
	pd.read_csv("incidents.csv")
	.assign(Date=lambda data: pd.to_datetime(data["DATE"], format="%Y-%m"))
	.sort_values(by="DATE")
)
countries = data["COUNTRY"].sort_values().unique()
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
                            value="Eng",
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
				),
				
			],
            className="menu",
        ),
        html.Div(
            children=[
				html.Div(
					[
						dbc.Card([
							dbc.CardHeader("This is the header of the card"),
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

@app.callback(
    Output("incidents-chart", "figure"),
    Output("datatable", "data"),
	Input("region-filter", "value"),
	Input("type-filter", "value"),
	Input("moving-average", "checked")
)
def update_charts(country, charttype, checked):
	filtered_data = data
	if country:
		filtered_data = data.query(
			"COUNTRY == @country"
		)
	gb_filtered_data = filtered_data.groupby('DATE').size().reset_index(name='num_of_incidents')
	gb_filtered_data = cast_date_str_to_date_and_sort(gb_filtered_data)
	
	data_list = [
		{
			"x": gb_filtered_data["DATE"],
			"y": gb_filtered_data["num_of_incidents"],
			"type": charttype,
		}
	]
	if checked:
		gb_filtered_data['moving_average'] = gb_filtered_data['num_of_incidents'].rolling(3).mean()
		data_list.append({
			"x": gb_filtered_data["DATE"],
			"y": gb_filtered_data["moving_average"],
			"type": "line",
			'line': {'color':'red'}
		})
		
	incidents_chart_figure = {
        "data": data_list,
		"layout": {
            "title": {
                "text": f"Number of incidents in {country}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
	filtered_data = filtered_data[['DATE', 'COUNTRY', 'INCIDENT_ID']]
	filtered_data['DATE'] = pd.to_datetime(filtered_data['DATE']).dt.strftime('%Y-%m')
	filtered_data.sort_values(by='DATE', inplace=True)
	datatable = filtered_data.to_dict(orient='records')
	return incidents_chart_figure, datatable


if __name__ == "__main__":
    app.run_server(debug=True)
	