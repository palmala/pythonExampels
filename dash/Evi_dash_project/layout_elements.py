#!/usr/bin/env python3
from dash import dcc, html, dash_table, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from abc import ABC


class LayoutElements(ABC):
    def __init__(self, df, column_to_dropdown):
        self.df = df
        self.column_to_dropdown = column_to_dropdown


class SimpleLayoutElements(LayoutElements):
    def __init__(self, df, column_to_dropdown='COUNTRY'):
        super().__init__(df, column_to_dropdown)
        self.inputs = []
        self.outputs = []
        self.header_div = self.create_header_div("Incident Analytics")
        self.buttons_in_menu = self.create_layout_menu_elements()
        self.range_slider_div = self.create_range_slider_div()
        self.graph = self.create_graph()
        self.data_table_for_incidents = self.create_data_table_for_incidents()

    def create_dropdown_button_with_column_values(self, column_name, button_label_name):
        values = self.df[column_name].sort_values().unique()
        return [{"label": value, "value": value} for value in values]

    def create_header_div(self, title):
        return html.Div(
            children=[
                html.H1(children=title, className="header-title"),
                html.P(
                    children=(
                        "Analyze the number of incidents"
                        " amongst different countries between 2021 and 2022"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        )

    def create_region_filter(self, country_dropdown_options):
        component_id = "region-filter"
        component_property = "value"
        self.inputs.append(Input(component_id, component_property))
        return html.Div(
            children=[
                html.Div(children="Country", className="menu-title"),
                dcc.Dropdown(
                    id=component_id,
                    options=country_dropdown_options,
                    value="ENG",
                    clearable=False,
                    className="dropdown",
                ),
            ]
        )

    def create_range_slider_div(self):
        input_component_id = "my-range-slider"
        input_component_property = "value"
        output_component_id = "output-container-range-slider"
        output_component_property = "children"
        self.inputs.append(Input(input_component_id, input_component_property))
        self.outputs.append(Output(output_component_id, output_component_property))

        return html.Div(
            [
                dcc.RangeSlider(10, 300, 50, value=[10, 300], id=input_component_id),
                html.Div(id=output_component_id),
            ],
            style={"width": "49%", "background": "gray"},
        )

    def create_moving_average_checkbox_div(self):
        component_id = "moving-average"
        component_property = "checked"
        self.inputs.append(Input(component_id, component_property))
        return html.Div(
            [
                dmc.Checkbox(id=component_id, label="Show moving average", mb=10),
            ]
        )

    def create_graph(self):
        component_id = "incidents-chart"
        component_property = "figure"
        self.outputs.append(Output(component_id, component_property))

        return dcc.Graph(
            id=component_id,
            config={"displayModeBar": False},
        )

    def create_data_table_for_incidents(self):
        component_id = "datatable"
        component_property = "data"
        self.outputs.append(Output(component_id, component_property))

        return dbc.Container(
            [
                dbc.Label("Data in table"),
                dash_table.DataTable(id=component_id),
            ]
        )

    def create_layout_menu_elements(self):
        country_dropdown_options = self.create_dropdown_button_with_column_values(
            self.column_to_dropdown, self.column_to_dropdown
        )
        country_dropdown_options.append({"label": "ALL", "value": ""})
        region_filter_div = self.create_region_filter(country_dropdown_options)
        moving_average_checkbox_div = self.create_moving_average_checkbox_div()
        return [region_filter_div, moving_average_checkbox_div]


class ComplexLayoutElements(SimpleLayoutElements):
    def __init__(self, df, column_to_dropdown='COUNTRY'):
        super().__init__(df, column_to_dropdown)

    def create_header_div(self, title):
        return super().create_header_div("Complex Incident Analytics")

    def create_chart_type_filter_div(self, chart_types):
        component_id = "type-filter"
        component_property = "value"
        self.inputs.append(Input(component_id, component_property))
        return html.Div(
            children=[
                html.Div(children="Chart Type", className="menu-title"),
                dcc.Dropdown(
                    id=component_id,
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

    def create_layout_menu_elements(self):
        chart_types_dropdown_options = ["line", "bar"]
        chart_type_filter = self.create_chart_type_filter_div(
            chart_types_dropdown_options
        )
        layout_menu_elements = super().create_layout_menu_elements()
        layout_menu_elements.append(chart_type_filter)
        return layout_menu_elements
	