import subprocess
import time

import logging_config
import data_prep
import data_analysis
import db_conn
import visuals

def stop_circusd():
    ''' Subprocess is used to stop the circusd watcher as the code will be exeucted over and over
        if this isn't done - I only want the code to run once without the need to have an open SSH
        connection so the code can be run while I'm not around.
    '''

    logger.info('Code has finished, stopping Circusd watcher')
    subprocess.call(['circusctl', 'stop', 'github-big-data'])


''' Various booleans used to trigger specific pieces of code that need to be run
    Good for running sections of the code when debugging, without having to change code in the
    'main' function below
'''
CREATE_TABLE = False
CSV_TO_PYTHON = False
CSV_TO_SQL = False
GET_DATA_FROM_SQL = True
VISUALISE_DATA = True
GET_DAILYS_FROM_SQL = False


logger = logging_config.setup_logging()

if __name__ == '__main__':
    logger.info('Start of new run')

    conn = db_conn.open_db_connection()

    if CREATE_TABLE:
        logger.info('About to create table in database')
        db_conn.create_table(conn)

    if CSV_TO_PYTHON:
        logger.info('About to take CSV data into Python')
        dataset = data_prep.get_data_from_csv()

    if CSV_TO_SQL:
        logger.info('About to go from CSV to SQL')
        data_prep.data_into_sql(conn)

    if GET_DATA_FROM_SQL:
        logger.info('Getting monthly chunks from SQL')
        monthly_chunks = data_analysis.get_monthly_chunks(conn)

    if GET_DAILYS_FROM_SQL:
        logger.info('Getting daily data from SQL')
        data_analysis.get_daily_chunks(conn)

    if VISUALISE_DATA:
        logger.info('Visualing data using Matplotlib')
        figures = visuals.plot_data(monthly_chunks)
        pdf_filename = visuals.export_as_pdf(figures)
        visuals.email_file(pdf_filename)



    # Write it out to a file
    #data_prep.store_clean_dataset(dataset)
    
    
# Stop Circusctl process from repeating code
stop_circusd()
