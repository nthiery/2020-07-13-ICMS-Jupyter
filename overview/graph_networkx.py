"""
A convenience wrapper around networkx's constructor
for (some) compatibility with our own graph class.

The compatibility is relatively limited. For example the edges methods
is richer in networkx, but does not include the capacity, nor reverse
edges for undirected graphs.

We test the compatibility of the basic methods on all the examples::

    >>> import graph, graph_networkx
    >>>
    >>> for G, GN in zip( graph.examples.all(), graph_networkx.examples.all() ):
    ...    assert G.is_directed() == GN.is_directed()
    ...    assert tuple(G.vertices()) == GN.vertices()
    ...    assert G.vertex_number() == GN.vertex_number()
    ...    #assert G.edge_number() == GN.edge_number()
    ...    for v in G.vertices():
    ...        assert set(G.neighbors_out(v)) == set(GN.neighbors(v))
    ...    for v1, v2, c in G.edges():
    ...        assert GN.is_edge(v1, v2)
    ...    for v1, v2 in GN.edges():
    ...        assert G.is_edge(v1, v2)
    ...    H = G.networkx()
    ...    assert H.vertices() == GN.vertices()
    ...    assert H.edges()    == GN.edges()
    ...    assert H.is_directed() == GN.is_directed()
"""

import networkx

import warnings

def Graph(vertices, edges, directed=False):
    if directed:
        G = networkx.DiGraph()
    else:
        G = networkx.Graph()
    G.add_nodes_from(vertices)
    if edges:
        if len(edges[0]) == 2:
            G.add_edges_from(edges)
        else:
            G.add_weighted_edges_from(edges)
    return G

def show(self):
    """
    Return a bqplot widget representing the graph
    """
    import bqplot.marks
    from ipywidgets import Layout
    import traitlets
    nodes = self.vertices()
    edges = self.edges()
    node_data = [ str(i) for i in nodes ]
    rank = { v: i for i,v in enumerate(nodes) }
    link_data = [{'source': rank[edge[0]],
                  'target': rank[edge[1]],
                 } for edge in edges]
    colors = ["white" for node in nodes]

    try:
        # ignore a FutureWarning in numpy raised
        # by networkx's planar_layout
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            layout = networkx.planar_layout(self)
    except networkx.NetworkXException:
        layout = networkx.spring_layout(self)
    xs = bqplot.LinearScale()
    ys = bqplot.LinearScale()
    x = [layout[node][0] for node in nodes]
    y = [layout[node][1] for node in nodes]

    fig_layout = Layout(width='400px', height='400px')
    mark = bqplot.marks.Graph(node_data=node_data,
                              link_data=link_data,
                              link_type='line', directed=self.is_directed(),
                              scales={'x': xs, 'y': ys, }, x=x, y=y,
                              colors=colors,
                              charge=-600)
    return bqplot.Figure(marks=[mark],
                         layout=fig_layout)

def vertices(self):
    return tuple(self.nodes())
networkx.Graph.vertices = vertices
networkx.DiGraph.vertices = vertices
networkx.Graph.vertex_number = networkx.Graph.number_of_nodes
networkx.DiGraph.vertex_number = networkx.DiGraph.number_of_nodes
networkx.Graph.edge_number = networkx.Graph.number_of_edges
networkx.DiGraph.edge_number = networkx.DiGraph.number_of_edges
networkx.Graph.is_edge = networkx.Graph.has_edge
networkx.DiGraph.has_edge = networkx.DiGraph.has_edge
networkx.Graph.show = show
networkx.DiGraph.show = show
networkx.Graph.neighbors_out = networkx.Graph.neighbors
networkx.DiGraph.neighbors_out = networkx.DiGraph.neighbors

import graph_examples
examples = graph_examples.Examples(Graph)
