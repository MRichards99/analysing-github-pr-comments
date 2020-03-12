import codecs
import csv
import lzma
import logging
import sys
from datetime import datetime

logger = logging.getLogger('big-data-python')
REVIEW_COMMENTS_PATH = "/home/xfu59478/big-data-work/review_comments.csv.xz"


def data_into_sql(conn):
    ''' Take dataset from CSV file and put it into SQL database.
        This function involves cleaning the dataset
    '''
    with lzma.open(REVIEW_COMMENTS_PATH) as f:
        dataset = csv.DictReader(codecs.getreader("utf-8")(f))
        cursor = conn.cursor()

        record_num = 0
        for record in dataset:
            record_num += 1

            # Is there a value in this record which is null?
            include_record = True
            for value in record.values():
                if value is None:
                    include_record = False
                    break

            # If one part of the record is null, remove entire record from dataset
            if not include_record:
                logger.info('Excluding this record due to null value. Comment ID: {}'.format(record['COMMENT_ID']))
                logger.debug('Data regarding excluded record: {}'.format(record.items()))
                continue

            # Convert from string to datetime object
            created_at_conv = datetime.strptime(record['CREATED_AT'], '%Y-%m-%dT%H:%M:%SZ')

            add_data = ("INSERT INTO pr_comments "
                        "(COMMENT_ID, COMMIT_ID, URL, AUTHOR, CREATED_AT, BODY) "
                        "VALUES (%(COMMENT_ID)s, %(COMMIT_ID)s, %(URL)s, %(AUTHOR)s, %(CREATED_AT)s, %(BODY)s)")

            data_dict = {
                'COMMENT_ID': record['COMMENT_ID'],
                'COMMIT_ID': record['COMMIT_ID'],
                'URL': record['URL'],
                'AUTHOR': record['AUTHOR'],
                'CREATED_AT': created_at_conv,
                'BODY': record['BODY']
            }

            cursor.execute(add_data, data_dict)

            if record_num % 100000 == 0:
                logger.debug('Just inserted data from record number: {}'.format(record_num))
                logger.debug('Information regarding this record: {}'.format(record.items()))


        # Commit SQL changes once all inserted - this will prevent duplicates in the event of an error
        conn.commit()



def store_dataset(dataset):
    ''' Store dataset stored in memory to text file
    '''
    with open('/home/xfu59478/big-data-work/analysing-github-pr-comments/dataset.txt', 'wb') as file:
        for record in dataset:
            file.write('{}\n'.format(record).encode('utf-8'))
