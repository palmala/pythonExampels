#!/usr/bin/env python3

from dash import Dash
import pandas as pd
from layout_elements import SimpleLayoutElements, ComplexLayoutElements
from layout_maker import SimpleLayoutMaker, ComplexLayoutMaker



if __name__ == "__main__":
	df = pd.read_csv('incidents2.csv')
	app = Dash(__name__)
	
	complex_layout_elements = ComplexLayoutElements(df)
	complex_layout_maker = ComplexLayoutMaker(app, df, 'ComplexEviProj', complex_layout_elements)
	complex_layout_maker.make_layout()

	app.run_server(debug=True)
	