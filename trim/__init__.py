import graph


class GraphTrimmer(object):
    '''
    Used to trim graphs so each edge as at most <n> outgoing vertices, sorted by weight, ascending.
    '''

    def trim(self, input_graph, max_vertices, on_status_update=None):
        '''
        :param input_graph: graph to iterate over. does not mutate
        :param max_vertices: maximum outgoing vertices per edge
        :param on_status_update: callback to report progress to. gets amount of iterations as parameter. optional
        :type on_status_update: callable(int)
        :return:
        '''
        update_ratio = 100
        iterations = 0

        # construct the trimmed graph as a new one
        output_graph = graph.Graph()

        # iterate over all vertices in the given graph
        for edge, vertices in input_graph.vertices.items():
            iterations += 1

            # notify callback if needed
            if iterations % update_ratio == 0 and callable(on_status_update):
                on_status_update(iterations)

            # sort vertices for given edge
            sorted_vertices = sorted(vertices.items(), key=lambda x: x[1])

            # trim vertices
            trimmed_vertices = sorted_vertices[:max_vertices]

            # construct new neighbours matrix
            neighbours = {neighbour: weight for neighbour, weight in trimmed_vertices}

            # set neighbours for given edge in the new graph
            output_graph.set_neighbours(edge, neighbours)

        return output_graph
