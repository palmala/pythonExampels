#!/usr/bin/env python3
import dash
from dash import callback
import pandas as pd
from layout_elements_for_multipages_app import SimpleLayoutElements
from layout_maker_for_multipages_app import SimpleLayoutMaker

dash.register_page(__name__)

df = pd.read_csv("incidents2.csv")
simple_layout_elements = SimpleLayoutElements(df)
simple_layout_maker = SimpleLayoutMaker(df, "DATE", "COUNTRY", simple_layout_elements)

layout = simple_layout_maker.make_layout()


@callback(
    simple_layout_maker.layout_elements.outputs,
    simple_layout_maker.layout_elements.inputs,
)
def update(country, moving_avg_checked, range_selector_value, charttype="line"):
    return simple_layout_maker.callback(
        country, moving_avg_checked, range_selector_value, charttype
    )
