#!/usr/bin/env python3
from dash import html
from dataframe_manipulation import (
    str_to_date_and_sort,
    fill_missing_dates_within_range,
    filter_data_between_min_and_max_value,
    filter_data_by_column_value,
    get_df_with_num_of_items_for_grouped_column_values,
    prepare_df,
)
from layout_elements import LayoutElements
from abc import ABC, abstractmethod


class LayoutMaker(ABC):
    def __init__(self, app, df, app_title, layout_elements):
        self.app = app
        self.df = df
        self.app.title = app_title
        self.layout_elements = layout_elements

    @abstractmethod
    def make_layout(self):
        pass

    @abstractmethod
    def callback(self):
        pass


class SimpleLayoutMaker(LayoutMaker):
    def __init__(self, app, df, app_title, layout_elements: LayoutElements):
        super().__init__(app, df, app_title, layout_elements)
        self.app.callback(self.layout_elements.outputs, self.layout_elements.inputs)(
            self.callback
        )

    def make_layout(self):
        prepare_df(self.df, "DATE", ["LIKES"])

        self.app.layout = html.Div(
            children=[
                self.layout_elements.header_div,
                html.Div(
                    children=self.layout_elements.buttons_in_menu,
                    className="menu",
                ),
                html.Div(
                    children=[
                        self.layout_elements.range_slider_div,
                        html.Div(
                            [
                                self.layout_elements.graph,
                                self.layout_elements.data_table_for_incidents,
                            ]
                        ),
                    ],
                    className="wrapper",
                ),
            ]
        )

    def create_data_list_for_chart(self, df, x, y, charttype):
        return [{"x": df[x], "y": df[y], "type": charttype}]

    def add_moving_average_date_to_data_list(
        self, df, x, y, column_to_have_moving_avg, data_list
    ):
        df[y] = df[column_to_have_moving_avg].rolling(3).mean()
        data_list.append(
            {"x": df[x], "y": df[y], "type": "line", "line": {"color": "red"}}
        )

    def create_date_filter_buttons(self):
        return [
            {"count": 6, "label": "6 month", "step": "month", "stepmode": "backward"},
            {"count": 1, "label": "1 year", "step": "year", "stepmode": "backward"},
            {"step": "all"},
        ]

    def create_chart_figure(self, data_list, chart_name):
        return {
            "data": data_list,
            "layout": {
                "title": {"text": chart_name, "x": 0.05, "xanchor": "left"},
                "colorway": ["#17B897"],
                "xaxis": {
                    "rangeselector": {"buttons": self.create_date_filter_buttons()},
                    "rangeslider": {"visible": True},
                    "type": "date",
                },
            },
        }

    def callback(
        self, country, moving_avg_checked, range_selector_value, charttype="line"
    ):
        min_value_of_likes = range_selector_value[0]
        max_value_of_likes = range_selector_value[1]
        filtered_data = filter_data_between_min_and_max_value(
            self.df, "LIKES", min_value_of_likes, max_value_of_likes
        )
        filter_data_by_column_value(filtered_data, "COUNTRY", country)
        gb_filtered_data = get_df_with_num_of_items_for_grouped_column_values(
            filtered_data, "DATE", "num_of_incidents"
        )
        str_to_date_and_sort(gb_filtered_data, "DATE")
        gb_filtered_data = fill_missing_dates_within_range(
            gb_filtered_data, "DATE", "MS", "%Y-%m"
        )
        data_list = self.create_data_list_for_chart(
            gb_filtered_data, "DATE", "num_of_incidents", charttype
        )
        if moving_avg_checked:
            self.add_moving_average_date_to_data_list(
                gb_filtered_data,
                "DATE",
                "moving_average",
                "num_of_incidents",
                data_list,
            )
        incidents_chart_figure = self.create_chart_figure(
            data_list, f"Number of incidents in {country}"
        )
        filtered_data = filtered_data[["DATE", "COUNTRY", "INCIDENT_ID", "LIKES"]]
        str_to_date_and_sort(filtered_data, "DATE", "%Y-%m")
        datatable = filtered_data.to_dict(orient="records")
        selector_str = (
            f"Filtered likes data from {min_value_of_likes} to {max_value_of_likes}"
        )

        return selector_str, incidents_chart_figure, datatable


class ComplexLayoutMaker(SimpleLayoutMaker):
    def __init__(self, app, df, app_title, layout_elements):
        super().__init__(app, df, app_title, layout_elements)

    def callback(self, charttype, country, moving_avg_checked, range_selector_value):
        return super().callback(
            country, moving_avg_checked, range_selector_value, charttype
        )
