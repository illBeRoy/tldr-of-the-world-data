import graph


class GraphTrimmer(object):

    def trim(self, input_graph, max_vertices, on_status_update=None):
        update_ratio = 100
        iterations = 0

        output_graph = graph.Graph()
        for edge, vertices in input_graph.vertices.iteritems():
            iterations += 1

            if iterations % update_ratio == 0 and callable(on_status_update):
                on_status_update(iterations)

            sorted_vertices = sorted(vertices.items(), key=lambda x: x[1])
            trimmed_vertices = sorted_vertices[:max_vertices]
            neighbours = {neighbour: weight for neighbour, weight in trimmed_vertices}

            output_graph.set_neighbours(edge, neighbours)

        return output_graph
