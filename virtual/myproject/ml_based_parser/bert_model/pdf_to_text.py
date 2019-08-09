from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

TEST = False


# the path to the pdf resume is the input to the code
def pdf_to_text(f_name, pages=None) -> list:
    """
    Parses PDF into list of strings containing lines of resume
    :param f_name: File to convert
    :param pages: Page to start with?(to confirm)
    :return: List of strings
    """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    # output = StringIO()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(f_name, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    # Output file is saved only when debugging
    # text_file = open("OutputZ.txt", "w")
    # text_file.write(text)
    # text_file.close()

    # Convert text into list
    line_list = [x for x in text.split('\n') if x.strip()]
    return line_list
