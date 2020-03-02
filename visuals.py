from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

def export_as_pdf(figures, pdf_path):
    current_datetime_str = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    filename = 'pr-comments-{}'.format(current_datetime_str)

    pdf_file = PdfPages('{}/{}'.format(pdf_path, filename))

    for figure in figures:
        figure.savefig(pdf_file, format='pdf')

    pdf_file.close()


def upload_files(filenames):
    ''' Take list of filenames, and send them across to my local machine - either via SCP or
        another method (Google Drive?)
    '''
    pass