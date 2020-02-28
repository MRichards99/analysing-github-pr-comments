import codecs
import csv
import lzma
import logging

logger = logging.getLogger('big-data-python')
REVIEW_COMMENTS_PATH = "/home/xfu59478/big-data-work/review_comments.csv.xz"


def get_data_from_csv():
    with lzma.open(REVIEW_COMMENTS_PATH) as f:
        comment_dataset = csv.DictReader(codecs.getreader("utf-8")(f))

        logger.debug(comment_dataset.fieldnames)

        num_rows = 0
        for record in comment_dataset:
            num_rows += 1
            if num_rows == 20:
                break

            logger.debug(record)

    return comment_dataset
