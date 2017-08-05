#!/usr/bin/env python
#
# The Generator Utility
#
# The generator utility is used in order to perform calculation over the pantheon.csv dataset, and export a directed,
# weighted graph that should indicate, for each person in the pantheon, which are the people that are most correlated
# to them.
#
# The calculations used are interchangeable, and you can add your own method of calculation by implementing a python
# file with WeightCalculator class (see examples under `calculators/`)
#

import csv
import itertools
import argparse
import imp
import progressbar

import graph
import trim


class Dataset(object):
    '''
    Parses CSV datasets and abstracts operations on top of them.

    Each row in the parsed dataset is represented as a dict, where the keys are the column titles and the values
    are the actual values of each row.
    '''

    def __init__(self, filename, sort_by=None):
        '''
        :param filename: name of csv file
        :param sort_by: name of column to sort rows by. optional
        '''
        self._rows = []

        with open('pantheon.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=',', dialect=csv.excel_tab)
            field_names = next(reader)

            for row_values in reader:
                row = {field_name: row_value for field_name, row_value in zip(field_names, row_values)}
                self._rows.append(row)

            if sort_by is not None:
                self._rows = sorted(self._rows, key=lambda x: x[sort_by])

    @property
    def rows(self):
        '''
        :return: rows of the dataset
        :rtype: list(dict)
        '''
        return self._rows

    @property
    def amount_of_pairs(self):
        '''
        :return: how many pairs of two different rows there could be
        :rtype: int
        '''
        amount_of_rows = len(self._rows)
        ncr_rows_choose_2 = amount_of_rows * (amount_of_rows - 1) / 2
        return ncr_rows_choose_2

    def get_column(self, column_name):
        '''
        :param column_name: name of the column
        :return: all values of all rows for the given column
        '''
        return [row[column_name] for row in self._rows]

    def map(self, fn, column_name):
        '''
        Applies a function to all rows in the dataset for a given column.

        :param fn: function to apply
        :param column_name: column to get data for
        :return: the result of the map function
        '''
        return list(map(fn, self.get_column(column_name)))


class GraphBuilder(object):
    '''
    Used to build a weighted graph between all rows in a given dataset, using a given calculator.
    '''

    def build_graph(self, dataset, calculator, notice_interval=10000, limit_rows=None, threshold=None):
        '''
        :param dataset: dataset object to build graph from
        :param calculator: calculator class to use for calculating weight of each vertex
        :param notice_interval: how many iterations should pass before updating the user. optional
        :param limit_rows: use only first n rows of the dataset. optional
        :param threshold: discard vertex if its weight is above this threshold. optional
        :return: weighted graph where rows['name'] are the edges
        '''
        data_graph = graph.Graph()

        rows = dataset.rows
        if limit_rows is not None:
            rows = rows[:limit_rows]

        bar = progressbar.ProgressBar(max_value=(len(rows) * (len(rows) - 1) / 2))
        bar.update(0)

        iterations = 0
        for a, b in itertools.combinations(rows, 2):
            iterations += 1
            if iterations % notice_interval == 0:
                bar.update(iterations)

            w = calculator.calculate(a, b)

            if threshold is not None and w > threshold:
                continue

            data_graph.add_vertex(a['wikiquote name'], b['wikiquote name'], w)

        bar.finish()

        return data_graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', help='name of dataset file', default='pantheon.csv')
    parser.add_argument('output', help='name of output graph file', default='graph.pickle')
    parser.add_argument('-ni', '--notice-interval', help='number of iterations for progress update', type=int, default=1000000)
    parser.add_argument('-lr', '--limit-rows', help='limits the number of rows used', type=int, required=False)
    parser.add_argument('-t', '--threshold', help='threshold weight. values larger than threshold are discarded', type=float, required=False)
    parser.add_argument('-mv', '--max-vertices', help='maximal outgoing vertices per edge', type=int, required=False)
    parser.add_argument('-wc', '--weight-calculator', help='name of file containing the WeightCalculator implementation', default='constant')
    args = parser.parse_args()

    # load dataset from csv
    csv_dataset = Dataset(args.dataset, sort_by='name')

    # load calculator from python module
    calculator = imp.load_source('calculator',
                                 './calculators/{0}.py'.format(args.weight_calculator))

    # build graph
    graph = GraphBuilder().build_graph(csv_dataset,
                                       calculator.WeightCalculator(),
                                       notice_interval=args.notice_interval,
                                       limit_rows=args.limit_rows,
                                       threshold=args.threshold)

    # if max_vertices were passed, trim graph so each edge has at most <max_vertices>, ordered by weight
    if args.max_vertices is not None:
        print('trimming graph to have {0} outgoing vertices per edge at most'.format(args.max_vertices))
        trimming_bar = progressbar.ProgressBar(max_value=len(graph.edges))

        graph = trim.GraphTrimmer().trim(graph, args.max_vertices, on_status_update=trimming_bar.update)

        trimming_bar.finish()

    # save graph to disk
    print('saving graph to disk...')
    graph.save(args.output)

    # done
    print ('\ndone')
