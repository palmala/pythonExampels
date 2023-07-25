#!/usr/bin/env python3

from dash import Dash
import pandas as pd
from layout_elements import SimpleLayoutElements, ComplexLayoutElements
from layout_maker import SimpleLayoutMaker, ComplexLayoutMaker



if __name__ == "__main__":
	df = pd.read_csv('incidents2.csv')
	app = Dash(__name__)
	
	simple_layout_elements = SimpleLayoutElements(df)
	simple_layout_maker = SimpleLayoutMaker(app, df, 'SimpleEviProj', simple_layout_elements)
	simple_layout_maker.make_layout()
	
	app.run_server(debug=True)
	