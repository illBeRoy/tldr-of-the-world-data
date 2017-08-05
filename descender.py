#!/usr/bin/env python
import argparse
import json
import jinja2
import webbrowser

import graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('groups', help='json file describing seed groups')
    args = parser.parse_args()

    # load group from file
    with open(args.groups, 'rb') as f:
        groups = json.loads(f.read())

    # load template from file
    with open('descender.html.jinja', 'rb') as f:
        template = jinja2.Template(f.read())

    # load graph from file
    graph = graph.Graph()
    graph.load('./graph.pickle')

    # find neighbours using the given groups and weight vector
    for group in groups:
        group['neighbours'] = graph.get_joint_neighbours(group['members'], group_size=50)
        group['neighbours'] = [''.join([c for c in x if ord(c) < 128]) for x in group['neighbours']]

    # generate output file
    with open('/tmp/descender.results.html', 'wb') as f:
        f.write(template.render({'groups': groups}))

    # open it
    webbrowser.open('file:///tmp/descender.results.html')
