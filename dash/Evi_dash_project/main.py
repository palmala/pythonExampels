#!/usr/bin/env python3
from app import app
from dash import html, dcc
import dash

app.layout = html.Div(
    [
        html.H1("Multi-pages Incident Analytics"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
