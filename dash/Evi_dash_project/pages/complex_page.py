#!/usr/bin/env python3

import dash
from dash import callback

from layout_elements_for_multipages_app import ComplexLayoutElements
from layout_maker_for_multipages_app import ComplexLayoutMaker
import pandas as pd

dash.register_page(__name__)
df = pd.read_csv("incidents3.csv")
complex_layout_elements = ComplexLayoutElements(df, "Region")
complex_layout_maker = ComplexLayoutMaker(df, "Date", "Region", complex_layout_elements)

layout = complex_layout_maker.make_layout()


@callback(
    complex_layout_maker.layout_elements.outputs,
    complex_layout_maker.layout_elements.inputs,
)
def update(country, moving_avg_checked, range_selector_value, charttype):
    return complex_layout_maker.callback(
        country, moving_avg_checked, range_selector_value, charttype
    )
