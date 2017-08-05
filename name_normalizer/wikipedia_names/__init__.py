import wikipedia

import wikiquotes_names


class WikiNameNormalizer(wikiquotes_names.NameNormalizer):

    def __init__(self, base_csv):
        super(WikiNameNormalizer, self).__init__(base_csv)

    def _start_polling(self):
        self._load_persons_and_locations('pantheon_wikiquotes_wikipedia.csv', 'wikipedia name')

    def _is_in_site(self, row):
        original_name = row[16]
        wikiquotes_name = row[23]
        try:
            result = wikipedia.page(original_name)
            return original_name
        except Exception as e:
            print('original name - {0}: {1}'.format(original_name, e))

        try:
            result = wikipedia.page(wikiquotes_name)
            return wikiquotes_name
        except Exception as e:
            print('{0}: {1}'.format(wikiquotes_name, e))

        return False

if __name__ == '__main__':
    normalizer = WikiNameNormalizer('../pantheon_wikiquotes.csv')
