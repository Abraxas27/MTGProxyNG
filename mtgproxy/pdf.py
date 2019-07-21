import sys
import os
import math

# Inspired from https://github.com/promisedlandt/mtg_proxy_printer/

ROOT_DIR = os.path.join(os.getcwd(), '..')

try:
    import reportlab
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
except ImportError:
    print('ReportLab not installed. Go to http://www.reportlab.org/')
    sys.exit(1)


def print_pdf(output_file_name, file_list):
    canvas = Canvas(output_file_name, pagesize=A4)
    # card size in mm
    CARD_WIDTH = 63
    CARD_HEIGHT = 88
    CARDS_ON_PAGE = 9

    padding_left = (A4[0] - 3 * CARD_WIDTH * mm) / 2
    padding_bottom = (A4[1] - 3 * CARD_HEIGHT * mm) / 2

    def make_page(page, canvas, file_list=()):
        # print("Page : " + str(page))
        canvas.translate(padding_left, padding_bottom)
        x, y = 0, 3
        canvas.drawString(x, y, '')
        # Pour les x cartes de la page
        for i in range(1, CARDS_ON_PAGE + 1):
            index = i + 9*(page - 1)
            # S'il reste des cartes
            if index <= len(file_list):
                # print("Index : " + str(index))
                image = file_list[index - 1]
                if x % 3 == 0:
                    y -= 1
                    x = 0
                # x and y define the lower left corner of the image you wish to
                # draw (or of its bounding box, if using preserveAspectRation below).
                canvas.drawImage(image, x=x * CARD_WIDTH * mm, y=y * CARD_HEIGHT * mm, width=CARD_WIDTH * mm,
                                 height=CARD_HEIGHT * mm)
                x += 1
            else:
                break
        canvas.showPage()

    def number_of_pages(size):
        return int(math.ceil(1.0 * size / CARDS_ON_PAGE))

    for page in range(1, number_of_pages(len(file_list))+1):
        make_page(page, canvas, file_list)

    try:
        canvas.save()
    except IOError:
        print('Save of the file {} failed. If you have the PDF file opened, close it.'.format(output_file_name))

    print('{} saved.'.format(output_file_name))
