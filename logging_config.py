import logging
import sys

def exception_log_handler(type, value, tb):
    logger = logging.getLogger('big-data-python')
    logger.exception('''Type: {} \n
                        Value: {} \n
                        Traceback: {}
                     '''.format(type, value, tb))


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

    # Override sys.excepthook to log all uncaught exceptions
    sys.excepthook = exception_log_handler

    return logger