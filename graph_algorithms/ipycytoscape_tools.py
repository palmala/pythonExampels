import ipycytoscape


def set_default_cytoscape_style(cytoscape_obj):
    cytoscape_obj.set_style(
        [
            {
                'selector': 'node',
                'style': {
                    'font-family': 'helvetica',
                    'font-size': 'data(fontsize)',
                    'label': 'data(label)',
                    'width': 'data(size)',
                    'height': 'data(size)',
                    'background-color': 'lightblue',
                    "text-valign": "center",
                    "text-halign": "center",
                }
            },
            {
                "selector": "edge.directed",
                "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle"
                },
            },
            {
                "selector": "edge.violation",
                "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    "line-color": "red",
                    "target-arrow-color": "red"
                },
            },
            {
                "selector": "edge.cycle",
                "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    "line-color": "purple",
                    "target-arrow-color": "purple"
                },
            }
        ]
    )
