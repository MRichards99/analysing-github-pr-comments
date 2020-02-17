import subprocess
import time
import logging

def stop_circusd():
    ''' Subprocess is used to stop the circusd watcher as the code will be exeucted over and over
        if this isn't done - I only want the code to run once without the need to have an open SSH
        connection so the code can be run while I'm not around.
    '''

    time.sleep(5)
    print('Code has finished, stopping Circusd watcher')
    subprocess.call(['circusctl', 'stop', 'github-big-data'])


def setup_logging():
    ''' Log output to an external file as part of the work for Circusd to allow code to be run
        without an active terminal
    '''
    LOG_DEBUG_PATH = '/var/log/analysing-github-pr-comments/debug.log'
    LOG_INFO_PATH = '/var/log/analysing-github-pr-comments/info.log'

    logger = logging.getLogger('big-data-python')
    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handlers = {'debug': [LOG_DEBUG_PATH, logging.DEBUG], 'info': [LOG_INFO_PATH, logging.INFO]}

    for handler in file_handlers.values():
        # Element 0: path to log file, element 1: logging level
        fh = logging.FileHandler(handler[0])
        fh.setLevel(handler[1])
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    return logger


logger = setup_logging()

if __name__ == '__main__':
    logger.info('Start of new run')
    



    
# Stop Circusctl process from repeating code
stop_circusd()