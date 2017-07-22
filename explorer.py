#!/usr/bin/env python
import argparse

import graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', help='file containing the graph information', default='graph.pickle')
    args = parser.parse_args()

    graph = graph.Graph()
    graph.load(args.graph)

    query = ''
    while True:
        query = raw_input('query> ')

        if query == 'exit':
            break

        elif query[0] == '~':
            results = filter(lambda x: query[1:] in x.lower(), graph.edges)
            print ', '.join(results)

        else:
            query = ' '.join(['{0}{1}'.format(q[0].upper(), q[1:].lower()) for q in query.split(' ')])

            try:
                neighbours = graph.get_neighbours(query)
            except:
                print 'Query failed: no entry named "{0}"'.format(query)
                continue

            result = sorted(neighbours.items(), key=lambda x: x[1])
            for res in result[:10]:
                print '{0} :: {1}'.format(res[0], res[1])

    print 'bye'
