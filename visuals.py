import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import logging
import subprocess
import os
import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger('big-data-python')

PDF_PATH = '/home/xfu59478/big-data-work/pdf-plots'

def plot_data(monthly_chunks):
    month_nums, str_dates, comment_count = monthly_chunks
    logger.info('{}, {}, {}'.format(len(month_nums), len(str_dates), len(comment_count)))

    np_dates = np.array(month_nums)
    np_comments = np.array(comment_count)
    m, b = np.polyfit(np_dates, np_comments, 1)

    logger.info('Slope of line of best fit: {}'.format(m))
    logger.info('Y-intercept of line of best fit: {}'.format(b))

    figure = plt.figure()

    #plt.plot(str_dates, comment_count)
    plt.plot(np_dates, np_comments)
    plt.plot(np_dates, m*np_dates + b, linestyle=':')

    plt.title('Pull Request Review Comments Over Time (2015-2018)')
    plt.xlabel('Time (Monthly)')
    plt.ylabel('Number of Pull Request Review Comments')
    plt.xticks(ticks=[0,11,23,35,47], labels=['01-2015', '12-2015', '12-2016', '12-2017', '12-2018'])

    figures = [figure]

    # Calculating Pearson's coefficient
    p_dict = {'dates': month_nums, 'comments': comment_count}
    p_data = pd.DataFrame(p_dict, columns=['dates', 'comments'])
    pearson_coef, p_value =stats.pearsonr(p_data['dates'], p_data['comments'])
    logger.info('Pearson\'s Correlation Coefficient: {}, P-Value: {}'.format(pearson_coef, p_value))

    return figures


def export_as_pdf(figures):
    current_datetime_str = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    filename = 'pr-comments-{}.pdf'.format(current_datetime_str)
    pdf_file = PdfPages('{}/{}'.format(PDF_PATH, filename))

    for figure in figures:
        figure.savefig(pdf_file, format='pdf')

    pdf_file.close()

    return filename


def email_file(filename):
    ''' Take list of filenames, and send them across to my local machine - either via SCP or
        another method (Google Drive?)
    '''

    #email_address = os.environ.get('PR_DATA_EMAIL_ADDRESS')
    email_address = 'matthew.richards@stfc.ac.uk'
    logger.debug('Email address: {}'.format(email_address))
    subprocess_cmd = ['mail', '-a', '{}/{}'.format(PDF_PATH, filename), '-s', filename,
                     email_address, '<', '/dev/null']
    logger.debug('Subprocess going to execute: {}'.format(subprocess_cmd))
    subprocess.call(subprocess_cmd)
