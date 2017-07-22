#!/usr/bin/env python
import csv
import itertools
import argparse
import imp
import progressbar

import graph
import trim


class Dataset(object):

    def __init__(self, filename, sort_by=None):
        self._rows = []

        with open('pantheon.csv', 'rU') as f:
            reader = csv.reader(f, delimiter=',', dialect=csv.excel_tab)
            field_names = next(reader)

            for row_values in reader:
                row = {field_name: row_value for field_name, row_value in zip(field_names, row_values)}
                self._rows.append(row)

            if sort_by is not None:
                self._rows = sorted(self._rows, key=lambda x: x[sort_by])

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, val):
        self._rows = val

    @property
    def max_connections(self):
        amount_of_rows = len(self._rows)
        ncr_rows_choose_2 = amount_of_rows * (amount_of_rows - 1) / 2
        return ncr_rows_choose_2

    def get_column(self, column_name):
        return [row[column_name] for row in self._rows]

    def map(self, fn, column_name):
        return map(fn, self.get_column(column_name))

    def save(self, filename):
        with open(filename, 'wb') as f:
            writer = csv.writer(f, delimiter=',', dialect=csv.excel_tab)
            writer.writerow(self._rows[0].keys())
            for row in self._rows:
                writer.writerow(row.values())


class GraphBuilder(object):

    def build_graph(self, dataset, calculator, notice_interval=10000, limit_rows=None, threshold=None):
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

            data_graph.add_vertex(a['name'], b['name'], w)

        return data_graph

    def calculate_weight(self, a, b):
        return 1.0


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

    csv_dataset = Dataset(args.dataset, sort_by='name')
    calculator = imp.load_source('calculator',
                                 './calculators/{0}.py'.format(args.weight_calculator))

    graph = GraphBuilder().build_graph(csv_dataset,
                                       calculator.WeightCalculator(),
                                       notice_interval=args.notice_interval,
                                       limit_rows=args.limit_rows,
                                       threshold=args.threshold)

    if args.max_vertices is not None:
        print 'trimming graph to have {0} outgoing vertices per edge at most'.format(args.max_vertices)
        trimming_bar = progressbar.ProgressBar(max_value=len(graph.edges))

        graph = trim.GraphTrimmer().trim(graph, args.max_vertices, on_status_update=trimming_bar.update)

        trimming_bar.finish()

    print 'saving graph to disk...'
    graph.save(args.output)

    print ('\ndone')
