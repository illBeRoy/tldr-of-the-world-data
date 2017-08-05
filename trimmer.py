#!/usr/bin/env python
#
# The Trimmer Utility
#
# Used for trimming an already existing graph.
#

import argparse
import progressbar

import graph
import trim


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input file to trim')
    parser.add_argument('max_vertices', help='maximum vertices per edge', type=int)
    args = parser.parse_args()

    graph = graph.Graph()

    print('loading graph from disk...')
    graph.load(args.input)

    print('updating neighbours map...')
    bar = progressbar.ProgressBar(max_value=len(graph.edges))

    trimmed_graph = trim.GraphTrimmer().trim(graph, args.max_vertices, on_status_update=bar.update)

    bar.finish()

    print('saving graph to disk...')
    filename_without_ext, ext = args.input.rsplit('.', 1)
    filename_without_ext = '{0}_trim_{1}'.format(filename_without_ext, args.max_vertices)
    trimmed_filename = '{0}.{1}'.format(filename_without_ext, ext)

    trimmed_graph.save(trimmed_filename)

    print('done')
