import codecs
import csv
import lzma
import logging

logger = logging.getLogger('big-data-python')


REVIEW_COMMENTS_PATH = "/home/xfu59478/big-data-work/review_comments.csv.xz"

def get_num_records():
    with lzma.open(REVIEW_COMMENTS_PATH) as archf:
        reader = csv.DictReader(codecs.getreader("utf-8")(archf))

        num_rows = 0
        for record in reader:
            num_rows += 1
            if num_rows % 50000 == 0:
                logger.debug('Row number: {}'.format(num_rows))
            

        logger.info('Number of records: {}'.format(num_rows))
    
    return num_rows