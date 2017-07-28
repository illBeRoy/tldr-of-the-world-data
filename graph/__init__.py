# NOTE: I mistakenly switched between "edges" and "vertices". therefore, everything that's called an "edge" is
#       actually a vertex, and vice versa.

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

    def get_joint_neighbours(self, edges, weight_vector=(1.0, 1.0), limit=None):
        '''
        Rate all neighbours of all given edges by their affinity to the group as a whole.

        :param edges: edges to which query the neighbours
        :param weight_vector: a vector representing how much weight is given to each parameter, the first being
                              the weight for the joint proximity and the other is the weight given for the amount
                              of joint neighbours. default is the identity vector. optional
        :param limit: if set, will limit the size of the output. optional
        :return: neighbours that are affiliated with most neighbours
        '''

        # count neighbours occurrences by creating a list of all neighbours of all edges and then counting each
        # neighbour's appearances in that list
        joint_neighbours_count = collections.Counter(sum([self.get_neighbours(edge).keys() for edge in edges], []))

        # sum proximity of neighbours from all edges
        joint_neighbours_proximity = {}
        for neighbour, proximity in sum([self.get_neighbours(edge).items() for edge in edges], []):
            joint_neighbours_proximity[neighbour] = joint_neighbours_proximity.get(neighbour, 0) + proximity

        # and then average all, and normalize by dividing in the maximal possible value
        maximal_proximity_val = max(sum([self.get_neighbours(edge).values() for edge in edges], []))
        for neighbour, summed_proximity in joint_neighbours_proximity.iteritems():
            joint_neighbours_proximity[neighbour] = summed_proximity / (joint_neighbours_count[neighbour] * maximal_proximity_val)

        # now re-assign scores by applying the weight vector on both the proximity and the count,
        # and then summing them
        joint_neighbours_score = {}
        for neighbour in joint_neighbours_count.iterkeys():

            # create values vector for the individual neighbour
            values_vector = (joint_neighbours_proximity[neighbour], joint_neighbours_count[neighbour])

            # calculate the score scalar by applying the weight vector unto the values vector
            score_scalar = sum([v1 * v2 for v1, v2 in zip(weight_vector, values_vector)])

            # set the neighbours score accordingly
            joint_neighbours_score[neighbour] = score_scalar

        # order them by amount of occurrences in descending order
        ordered_neighbours = [neighbour_name for neighbour_name, score in sorted(joint_neighbours_score.items())]

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
