import logging
import data_prep

logger = logging.getLogger('big-data-python')

def get_num_records():
    dataset = data_prep.get_data_from_csv()

    num_rows = 0
    for record in dataset:
        num_rows += 1
        if num_rows % 1000000 == 0:
            logger.debug('Row number: {}'.format(num_rows))
        
    logger.info('Number of records: {}'.format(num_rows))
    
    return num_rows
