import cPickle as pickle


class Graph(object):

    def __init__(self):
        self._edges = set()
        self._vertices = {}

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices

    def add_vertex(self, a, b, weight):
        self._edges.add(a)
        self._edges.add(b)

        self._vertices[a] = self._vertices.get(a, {})
        self._vertices[b] = self._vertices.get(b, {})

        self._vertices[a][b] = weight
        self._vertices[b][a] = weight

    def get_neighbours(self, edge):
        try:
            return self._vertices[edge]
        except:
            raise Exception('No such edge')

    def set_neighbours(self, edge, neighbours):
        self._edges.add(edge)
        self._vertices[edge] = neighbours

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self._vertices, self._edges), f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self._vertices, self._edges = pickle.load(f)
