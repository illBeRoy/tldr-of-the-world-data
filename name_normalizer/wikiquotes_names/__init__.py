import wikiquote
import csv


class NameNormalizer(object):

    def __init__(self, base_csv):
        self._csv_file_path = base_csv
        self._start_polling()

    def _start_polling(self):
        self._load_persons_and_locations('pantheon_wikiquotes.csv', 'wikiquotes name')

    def _load_persons_and_locations(self, output_file_name, row_name):
        with open(self._csv_file_path, 'r', encoding='utf8') as input_file:
            with open('../{0}'.format(output_file_name), 'w', encoding='utf8') as output_file:
                reader = csv.reader(input_file, delimiter=',')

                all_rows = []
                row = next(reader)
                row.append(row_name)
                all_rows.append(row)

                for row in reader:
                    result = self._is_in_site(row)
                    if result is not False:
                        row.append(result)
                    all_rows.append(row)

                writer = csv.writer(output_file)
                writer.writerows(all_rows)

    def _is_in_site(self, row):
        name = row[16]
        try:
            wikiquote.quotes(name)
        except Exception as e:
            if e.__class__.__name__ != 'NoSuchPageException':
                print('{0}: {1}'.format(name, e))
            return False
        return name


if __name__ == '__main__':
    normalizer = NameNormalizer('../pantheon.csv')
