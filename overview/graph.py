# -*- coding: utf-8 -*-

class Graph:
    def __init__(self,
                 vertices=None,
                 matrix=None,
                 edges=None,
                 directed=False):
        """
        Initialisation d'un graphe

        INPUT :

            - vertices, un itérables sur les sommets du graphes
            - matrix, la matrice d'adjacence du graphe suivant les mêmes indices que `vertices`
            - edges, une liste de triplets (v1, v2, c) où v1 et v2 sont des sommets et c un nombre positif

        """
        if vertices is None:
            vertices = []

        self._vertices = vertices
        # création d'un dictionnaire associant son indice à chaque sommet
        # (vous pouvez modifier si ça n'est pas utile à votre implantation)
        self._vertex_indices = {vertices[i]: i for i in range(len(vertices))}
        self._directed = directed

        # on ne peut pas donner à la fois matrix et edges
        if matrix is not None and edges is not None:
            raise ValueError("'matrix' et 'edges' ne peuvent pas être tous les deux initialisés")

        # initialisation différenciée: implantez les méthodes en question
        if matrix is not None:
            self._init_from_matrix(matrix)
        elif edges is not None:
            self._init_from_edges(edges)
        else:
            self._init_empty()

    def _init_empty(self):
        """
        Initialisation d'un graphe vide (sans arêtes)
        """
        ### BEGIN SOLUTION
        self._neighbors_out = {u: {} for u in self._vertices }
        ### END SOLUTION


    def _init_from_matrix(self, matrix):
        """
        Initialisation à partir d'une matrice

        EXAMPLES:

            >>> M = matrix = [[0, 12,  0, 12],
            ...               [0,  0, 23, 0],
            ...               [0,  0,  0, 0],
            ...               [0,  0,  0, 0]]
            >>> G = Graph(vertices = ["A", "B", "C", "D"],
            ...           matrix = M,
            ...           directed = True)
            >>> G.edges()
            (('A', 'B', 12), ('A', 'D', 12), ('B', 'C', 23))
            >>> G.matrix() == M
            True
        """
        ### BEGIN SOLUTION
        edges = [(v1, v2, matrix[i1][i2])
                 for i1, v1 in enumerate(self._vertices)
                 for i2, v2 in enumerate(self._vertices)
                 if matrix[i1][i2]]
        self._init_from_edges(edges)
        ### END SOLUTION

    def _init_from_edges(self, edges):
        """
        Initialisation à partir d'une liste de triplets
        """
        # BEGIN SOLUTION
        self._init_empty()
        for u, v, value in edges:
            self._neighbors_out[u][v] = value
            if not self._directed:
                self._neighbors_out[v][u] = value
        # END SOLUTION

    def is_directed(self):
        """
        Renvoie si le graph est orienté
        """
        return self._directed

    def set_edge_capacity(self, v1, v2, c):
        """
        Donne la capacité `c` à l'arête `(v1,v2)`

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe
            - c la capacité de l'arête (v1,v2)
        """
        # à compléter

    def add_vertex(self, v):
        """
        Ajoute le sommet `v` au graphe

        INPUT:

            - v, un sommet du graphe

        """
        # à compléter

    def vertices(self):
        """
        Renvoie la liste des sommets du graphe

        EXAMPLES::

            >>> from graph import examples
            >>> G = examples.cours_1_reseau()
            >>> G.vertices()
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        """
        ### BEGIN SOLUTION
        return self._vertices
        ### END SOLUTION

    def vertex_number(self):
        """
        Renvoie le nombre de sommets du graphe

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> G.vertex_number()
            8
        """
        ### BEGIN SOLUTION
        return len(self._vertices)
        ### END SOLUTION

    def has_vertex(self, v1):
        """
        Renvoie vrai si v1 est un sommet du graphe

        INPUT:

            - v1, un sommet
        """
        # à compléter

    def edges(self):
        """
        Renvoie un tuple de triplets `(v1,v2,c)` correspondant aux arêtes du graphe avec leur capacité.

        EXAMPLES:

            >>> G = Graph((1,2,3,4))
            >>> G. edges()
            ()
            >>> G = examples.directed()
            >>> sorted(G.edges())
            [(1, 2, 12), (1, 4, 12), (2, 3, 23)]

            >>> G = examples.undirected()
            >>> sorted(G.edges())
            [(1, 2, 12), (2, 1, 12), (2, 3, 23), (3, 2, 23)]
        """
        ### BEGIN SOLUTION
        return tuple( (u, v, l)
                      for u, out in self._neighbors_out.items()
                      for v, l in out.items() )
        ### END SOLUTION

    def edge_number(self):
        """
        Renvoie le nombre d'arêtes du graphe
        """
        ### BEGIN SOLUTION
        return len(self.edges())
        ### END SOLUTION


    def is_edge(self, v1, v2):
        """
        Renvoie si l'arête (v1,v2) existe

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe
        """
        return v2 in self.neighbors_out(v1)

    def capacity(self, v1, v2):
        """
        Renvoie la capacité de l'arête (v1,v2) (si l'arête n'existe pas, la capacité est 0)

        INPUT:

            - v1, un sommet du graphe
            - v2, un sommet du graphe

        EXAMPLES::

            >>> G = examples.directed()
            >>> G.capacity(1,2)
            12
            >>> G.capacity(2,1)
            0
            >>> G.capacity(2,3)
            23
            >>> G.capacity(3,2)
            0
        """
        ### BEGIN SOLUTION
        return self._neighbors_out[v1].get(v2, 0)
        ### END SOLUTION


    def matrix(self):
        """
        Retourne la matrice associée au graphe

        Soit `n` le nombre de sommets du graphe. Cette méthode renvoie
        une liste `M` de n listes de taille n, de sorte que `M[i][j]`
        est la capacité de l'arête reliant le i-ème sommet au j-ème
        sommet dans le graphe, s'il y en a une, et 0 sinon.

        EXAMPLES::

            >>> G = examples.directed()
            >>> G.matrix()              # doctest: +NORMALIZE_WHITESPACE
            [[0, 12, 0, 12],
             [0, 0, 23, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
        """
        return [[ self.capacity(v1,v2)
                  for v2 in self.vertices() ]
                for v1 in self.vertices() ]

    def to_dict(self):
        """
        Retourne le dictionnaire associé au graphe
        """
        # à compléter

    def neighbors_in(self, v):
        """
        Renvoie la liste des voisins entrants de `v`

        INPUT:

            - v, un sommet du graphe

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> sorted(G.neighbors_in("H"))
            ['C', 'D', 'E', 'G']
            >>> G = examples.directed()
            >>> G.neighbors_in(1)
            ()
            >>> G.neighbors_in(2)
            (1,)
        """
        ### BEGIN SOLUTION
        return tuple( u for u in self._vertices if v in self._neighbors_out[u])
        ### END SOLUTION

    def neighbors_out(self, v):
        """
        Renvoie la liste des voisins sortants de `v`

        INPUT:

            - v, un sommet du graphe

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> sorted(G.neighbors_out("A"))
            ['B', 'F', 'G']
            >>> G = examples.directed()
            >>> sorted(G.neighbors_out(1))
            [2, 4]
            >>> G.neighbors_out(2)
            (3,)
            >>> G.neighbors_out(4)
            ()
        """
        ### BEGIN SOLUTION
        return tuple(self._neighbors_out[v].keys())
        ### END SOLUTION

    def is_path(self, p):
        """
        Renvoie si `p` est un chemin valide dans le graphe

        INPUT:

            - p, une liste de sommets du graphe

        EXAMPLES::

            >>> G = examples.cours_1_reseau()
            >>> G.is_path([])
            True
            >>> G.is_path(["D"])
            True
            >>> G.is_path(["D", "G"])
            False
            >>> G.is_path(["D", "H"])
            True
            >>> G.is_path(["D", "H", "F"])
            False
            >>> G.is_path(["D", "H", "G", "B", "A"])
            True
        """
        ### BEGIN SOLUTION
        for i in range(len(p)-1):
            if not self.is_edge(p[i], p[i+1]):
                return False
        return True
        ### END SOLUTION

    def networkx(self):
        import graph_networkx
        return graph_networkx.Graph(self.vertices(), self.edges(), directed=self.is_directed())

    def show(self):
        return self.networkx().show()

import graph_examples
examples = graph_examples.Examples(Graph)
