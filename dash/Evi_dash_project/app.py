#!/usr/bin/env python3

import pandas as pd
from dash import Dash, Input, Output, dcc, html


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
                            options=[
                                {"label": country, "value": country}
                                for country in countries
                            ],
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
				)
			],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                )
			],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
	Input("region-filter", "value"),
	Input("type-filter", "value"),
)

def update_charts(country, charttype):
	filtered_data = data.query(
        "COUNTRY == @country"
	)
	filtered_data = filtered_data.groupby('DATE').size().reset_index(name='num_of_incidents')
	filtered_data = cast_date_str_to_date_and_sort(filtered_data)
	price_chart_figure = {
        "data": [
            {
                "x": filtered_data["DATE"],
                "y": filtered_data["num_of_incidents"],
                "type": charttype,
#               "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"Num of incidents in {country}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
	return price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
	