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
# 3. [<Person Name>, ...<Person Name>] - searches for joint neighbours of specified people. case insensitive.
#                                        must be spelled exactly as it is in the graph.
#    example: [Ariel Sharon, Ehud Barak]
#
# 4. exit - closes the explorer app
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
        query = input('query> ')

        # break the loop
        if query == 'exit':
            break

        # return all relevant edges which contain the query's string
        elif query[0] == '~':
            results = [x for x in graph.edges if query[1:] in x.lower()]
            print(', '.join(results))

        # return all relevant edges which contain the query's string
        elif query[0] == '[' and query[-1] == ']':
            names = [word.strip().title() for word in query[1:-1].split(',')]

            try:
                result = graph.get_joint_neighbours(names, group_size=20)
            except Exception as err:
                print('Query failed: probably one of the queries did not yield results')
                continue

            for res in result:
                print(res)

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
            query = query.title()

            # find neighbours if query exists in graph
            try:
                neighbours = graph.get_neighbours(query)
            except:
                print('Query failed: no entry named "{0}"'.format(query))
                continue

            # sort neighbours by proximity (lower weight = higher proximity)
            result = sorted(list(neighbours.items()), key=lambda x: x[1])

            # print first ten results
            for res in result[:limit]:
                print('{0} :: {1}'.format(res[0], res[1]))

    print('bye')
