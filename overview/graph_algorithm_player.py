import bqplot.marks
import ipywidgets
import traitlets
import networkx
import warnings

from IPython.core.display import display
import value_player_widget

class GraphAlgorithmView(ipywidgets.VBox):

    def __init__(self, graph, variables=[]):
        if not isinstance(graph, (networkx.Graph, networkx.DiGraph)):
            graph = graph.networkx()
        self._graph = graph
        self._variables = variables

        nodes = graph.vertices()
        self._rank = { v: i for i,v in enumerate(nodes) }

        try:
            # ignore a FutureWarning in numpy raised
            # by networkx's planar_layout
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                layout = networkx.planar_layout(graph)
        except networkx.NetworkXException:
            layout = networkx.spring_layout(graph)
        xs = bqplot.LinearScale()
        ys = bqplot.LinearScale()
        cs = bqplot.ColorScale(scheme='Reds')
        x = [layout[node][0] for node in nodes]
        y = [layout[node][1] for node in nodes]

        fig_layout = ipywidgets.Layout(width='400px', height='400px')
        self._mark = mark = bqplot.marks.Graph(
            node_data = self.node_data(),
            link_type='line', directed=graph.is_directed(),
            scales={'x': xs, 'y': ys, 'link_color': cs},
            x=x, y=y,
            charge=-600,
            colors=self.colors())

        fig = bqplot.Figure(marks=[mark],
                            layout=fig_layout)

        self._variable_views={}
        variables_boxes = []
        for v in variables:
            label  = ipywidgets.Label(v['name'])
            output = ipywidgets.Output()
            self._variable_views[v['name']] = output
            variables_boxes.extend([label, output])
        variables_view = ipywidgets.GridBox(variables_boxes,
                                            layout = ipywidgets.Layout(grid_template_columns='1fr 1fr'))
        ipywidgets.VBox.__init__(self, [fig,
                                        variables_view])
        self.update()


    value = traitlets.Dict()

    @traitlets.default('value')
    def _default_value(self):
        return {}

    @traitlets.observe('value')
    def _observe_value(self, change):
        self.update()

    def colors(self):
        rank = self._rank
        colors = ['white'] * len(rank)
        for variable in self._variables:
            name  = variable['name']
            type  = variable.get('type','node')
            color = variable['color']
            values = self.value.get(name)
            if values is None:
                continue
            if type == 'list':
                nodes = self.value[name]
            else:
                nodes = [self.value[name]]
            for node in nodes:
                colors[rank[node]] = color
        return colors

    def node_data(self):
        return [str(i) for i in self._graph.nodes() ]
        # Fails: get a white image after the first image
        return [{'label': str(i)} for i in self._graph.nodes() ]
        # Fails: garbled edges after the first image
        def shape(i):
            if i == self.value.get('source', None):
                return "rect"
            elif i == self.value.get('target', None):
                return "ellipse"
            else:
                return "circle"
        return [ {'label':str(i),
                  'shape':shape(i)
                 }
                 for i in self._graph.nodes() ]

    def link_data(self):
        rank = self._rank
        #source = self.value.get('source', None)
        #target = self.value.get('target', None)
        return [{'source': rank[edge[0]],
                 'target': rank[edge[1]],
                 #'value': 255 if source == s and target == t else 0
                }
                for edge in self._graph.edges()]

    def update(self):
        link_data = self._mark.link_data
        self._mark.colors = self.colors()
        #self._mark.node_data = self.node_data()
        # Workaround to force an update
        self._mark.link_data = link_data + [{'source':0, 'target':0}]
        self._mark.link_data = self.link_data()

        for variable in self._variables:
            name  = variable['name']
            value = self.value.get(name)
            output = self._variable_views[name]
            output.clear_output(wait=True)
            with output:
                if value is not None:
                    display(value)

def GraphAlgorithmPlayer(graph, variables=[]):
    return value_player_widget.ValuePlayerWidget(
        GraphAlgorithmView(graph, variables=variables))
