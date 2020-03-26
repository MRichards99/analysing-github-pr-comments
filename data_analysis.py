import logging
import data_prep

logger = logging.getLogger('big-data-python')

def get_num_records():
    ''' Use dataset in CSV file to get number of records
    '''

    dataset = data_prep.get_data_from_csv()

    num_rows = 0
    for record in dataset:
        num_rows += 1
        if num_rows % 1000000 == 0:
            logger.debug('Row number: {}'.format(num_rows))
        
    logger.info('Number of records: {}'.format(num_rows))
    
    return num_rows


def get_monthly_chunks(conn):
    ''' Use an SQL query to get the number of comments in each month
    '''
    cursor = conn.cursor()
    chunk_query = """SELECT MONTH(CREATED_AT) AS StatMonth, YEAR(CREATED_AT) AS StatYear, 
                     COUNT(*) AS StatCount FROM pr_comments 
                     GROUP BY YEAR(CREATED_AT),  MONTH(CREATED_AT);
                  """
    cursor.execute(chunk_query)

    month_nums = []
    str_dates = []
    comment_count = []

    month_num = 0
    for StatMonth, StatYear, StatCount in cursor:
        logger.info('Month: {}, Year: {}, Count: {}'.format(StatMonth, StatYear, StatCount))

        str_date = '{}-{}'.format(StatMonth, StatYear)
        month_nums.append(month_num)
        str_dates.append(str_date)
        comment_count.append(StatCount)

        month_num += 1

    return (month_nums, str_dates, comment_count)

def get_daily_chunks(conn):
    ''' Use an SQL query to get the number of comments in each month
    '''
    cursor = conn.cursor()

    chunk_query = """
                  SELECT DAY(CREATED_AT) AS StatDay, MONTH(CREATED_AT) AS StatMonth, YEAR(CREATED_AT) AS StatYear,
                  COUNT(*) AS StatCount FROM pr_comments GROUP BY DAY(CREATED_AT), YEAR(CREATED_AT), MONTH(CREATED_AT)
                  ORDER BY YEAR(CREATED_AT), MONTH(CREATED_AT), DAY(CREATED_AT);
                  """
    cursor.execute(chunk_query)

    month_nums = []
    str_dates = []
    comment_count = []

    #month_num = 0
    for StatDay, StatMonth, StatYear, StatCount in cursor:
        logger.info('{}-{}-{} - {}'.format(StatDay, StatMonth, StatYear, StatCount))

        #str_date = '{}-{}'.format(StatMonth, StatYear)
        #month_nums.append(month_num)
        #str_dates.append(str_date)
        #comment_count.append(StatCount)

        #month_num += 1


    #return (month_nums, str_dates, comment_count)


