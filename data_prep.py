import codecs
import csv
import lzma
import logging
import sys

logger = logging.getLogger('big-data-python')
REVIEW_COMMENTS_PATH = "/home/xfu59478/big-data-work/review_comments.csv.xz"


def get_data_from_csv():
    ''' Open CSV, clean data to have in code
    '''
    with lzma.open(REVIEW_COMMENTS_PATH) as f:
        base_dataset = csv.DictReader(codecs.getreader("utf-8")(f))
        logger.debug(type(base_dataset))


        logger.debug(base_dataset.fieldnames)

        clean_dataset = []
        num_rows = 0
        for record in base_dataset:
            num_rows += 1
            #if num_rows == 2000000:
                #break

            # Retrieve required data to make a clean dataset
            clean_dataset.append([record['CREATED_AT'], record['BODY']])

        logger.debug('Inside clean dataset: {}'.format(clean_dataset[2143]))
        logger.debug('Size of dataset: {} bytes'.format(sys.getsizeof(clean_dataset)))

    return clean_dataset


def data_into_sql():
    pass

def store_clean_dataset(dataset):
    with open('/home/xfu59478/big-data-work/analysing-github-pr-comments/dataset.txt', 'wb') as file:
        for record in dataset:
            file.write('{}\n'.format(record).encode('utf-8'))
