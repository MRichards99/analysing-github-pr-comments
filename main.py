import subprocess
import time

import logging_config
import data_prep
import data_analysis

def stop_circusd():
    ''' Subprocess is used to stop the circusd watcher as the code will be exeucted over and over
        if this isn't done - I only want the code to run once without the need to have an open SSH
        connection so the code can be run while I'm not around.
    '''

    time.sleep(1)
    logger.info('Code has finished, stopping Circusd watcher')
    subprocess.call(['circusctl', 'stop', 'github-big-data'])



logger = logging_config.setup_logging()

if __name__ == '__main__':
    logger.info('Start of new run')
    data_prep.get_data_from_csv()
    
# Stop Circusctl process from repeating code
stop_circusd()
