import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
# from networkx.drawing.nx_agraph import graphviz_layout

PROJECTS = {
    'A': ['B', 'D'],
    'B': ['A'],
    'C': ['A'],
    'D': ['B', 'E'],
    'E': []
}


def main():
    G = nx.DiGraph(PROJECTS)
    pos = graphviz_layout(G, prog="dot")
    G.nodes(data=True)
    subax1 = plt.subplot(121)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    subax2 = plt.subplot(122)
    nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    main()
