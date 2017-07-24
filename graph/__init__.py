import cPickle as pickle
import collections


class Graph(object):
    '''
    Represents a directed, weighted, serializable graph.
    '''

    def __init__(self):
        self._edges = set()
        self._vertices = {}

    @property
    def edges(self):
        '''
        :return: edges of the graph
        :rtype: set(str)
        '''
        return self._edges

    @property
    def vertices(self):
        '''
        :return: vertices of the graph, where [a][b] = weight of the vertex (a, b)
        :rtype: dict(str, dict(str, float))
        '''
        return self._vertices

    def add_vertex(self, a, b, weight):
        '''
        Adds a new vertex to the graph, and possibly new edges.

        :param a: first edge
        :param b: second edge
        :param weight: weight of the vertex
        '''
        self._edges.add(a)
        self._edges.add(b)

        self._vertices[a] = self._vertices.get(a, {})
        self._vertices[b] = self._vertices.get(b, {})

        self._vertices[a][b] = weight
        self._vertices[b][a] = weight

    def get_neighbours(self, edge):
        '''
        Get all neighbouring edges (as vertices) for a given edge.

        :param edge: relevant edge
        :return: all vertices which come out of the edge, where [edge_2] = weight of the vertex (edge, edge_2)
        :rtype: dict(str, float)
        '''
        try:
            return self._vertices[edge]
        except:
            raise Exception('No such edge')

    def set_neighbours(self, edge, neighbours):
        '''
        Changes all outgoing vertices of a given edge to connect to the given neighbours with the given weights.

        NOTE: this may leave some other edge in the graph disconnected, as edges are not being removed automatically.

        :param edge: relevant edge
        :param neighbours: neighbouring edges and their vertices
        '''
        self._edges.add(edge)

        for neighbour in neighbours.iterkeys():
            self._edges.add(neighbour)

        self._vertices[edge] = neighbours

    def get_joint_neighbours(self, edges, limit=None):
        '''
        Rate all neighbours of all given edges by their affinity to the group as a whole.

        :param edges: edges to which query the neighbours
        :param limit: if set, will limit the size of the output. optional
        :return: neighbours that are affiliated with most neighbours
        '''

        # get all neighbours of all edges
        all_neighbours = sum([self.get_neighbours(edge).keys() for edge in edges], [])

        # count neighbours occurrences
        neighbours_counter = collections.Counter(all_neighbours)

        # order them by amount of occurrences in descending order
        ordered_neighbours = [neighbour_name for neighbour_name, count in reversed(sorted(neighbours_counter.items()))]

        # return the list, or part of it if there's a limit
        if limit is not None:
            return ordered_neighbours[:limit]
        else:
            return ordered_neighbours

    def save(self, filename):
        '''
        Saves graph to disk.

        :param filename: file to save graph into
        '''
        with open(filename, 'wb') as f:
            pickle.dump((self._vertices, self._edges), f)

    def load(self, filename):
        '''
        Loads graph from disk.

        :param filename: file to load graph from
        '''
        with open(filename, 'rb') as f:
            self._vertices, self._edges = pickle.load(f)
