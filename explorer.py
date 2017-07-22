#!/usr/bin/env python
#
# The Explorer Utility
#
# Lets you explore a generated graph by querying it: for a given person name, it returns the ten closest neighbours.
#
# Available queries and commands are:
# 1. <Person Name>[:x] - searches for that person. case insensitive. must be spelled exactly as it is in the graph.
#                        optionally followed by :x where x is the desired number of results to display.
#    example a: Ariel Sharon
#    example b: Ariel Sharon:20
#
# 2. ~<String> - searches for people whose names contain the given string.
#    example: ~sharon
#
# 3. exit - closes the explorer app
#

import argparse

import graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', help='file containing the graph information', default='graph.pickle')
    args = parser.parse_args()

    # load graph from file
    graph = graph.Graph()
    graph.load(args.graph)

    # main loop
    while True:
        query = raw_input('query> ')

        # break the loop
        if query == 'exit':
            break

        # return all relevant edges which contain the query's string
        elif query[0] == '~':
            results = filter(lambda x: query[1:] in x.lower(), graph.edges)
            print ', '.join(results)

        # find closest neighbours for the given name
        else:

            # try to extract limit from query. if it fails, it means that the user did not
            # specify it - so use the default limit value
            try:
                query, limit = query.split(':')
                limit = int(limit)
            except:
                limit = 10

            # normalize and capitalize query
            query = ' '.join(['{0}{1}'.format(q[0].upper(), q[1:].lower()) for q in query.split(' ')])

            # find neighbours if query exists in graph
            try:
                neighbours = graph.get_neighbours(query)
            except:
                print 'Query failed: no entry named "{0}"'.format(query)
                continue

            # sort neighbours by proximity (lower weight = higher proximity)
            result = sorted(neighbours.items(), key=lambda x: x[1])

            # print first ten results
            for res in result[:limit]:
                print '{0} :: {1}'.format(res[0], res[1])

    print 'bye'
