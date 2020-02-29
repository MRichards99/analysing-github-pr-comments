import subprocess
import time

import logging_config
import data_prep
import data_analysis
import db_conn

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


logger = logging_config.setup_logging()

if __name__ == '__main__':
    logger.info('Start of new run')

    conn = db_conn.open_db_connection()

    if CREATE_TABLE:
        db_conn.create_table(conn)

    if CSV_TO_PYTHON:
        dataset = data_prep.get_data_from_csv()

    # Write it out to a file
    #data_prep.store_clean_dataset(dataset)
    
    
# Stop Circusctl process from repeating code
stop_circusd()
