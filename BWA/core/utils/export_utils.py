import csv
import tempfile

import pdfkit
from django.http import HttpResponse
from django.http import StreamingHttpResponse

from MGL.settings import PATH_TO_WKHTMLTOPDF
from core import CoreConstantes

'''
Classe générique de gestion des download, exports : pdf, docx, csv, ...
'''


class ExportUtils:

    @staticmethod
    def download_page_as_pdf_from_html(html, filename=None):
        config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
        pdf_file = tempfile.NamedTemporaryFile(prefix=filename, suffix='.pdf', delete=False)
        pdfkit.from_string(html, pdf_file.name, configuration=config)
        return pdf_file.name

    @staticmethod
    def download_page_as_docx_from_html(html, filename=None):
        fullname_pdf = ExportUtils.download_page_as_pdf_from_html(html, filename)
        fullname_docx = fullname_pdf.replace(CoreConstantes.Extension.PDF.extension(), CoreConstantes.Extension.DOCX.extension())

        from pdf2docx import Converter
        cv = Converter(fullname_pdf)
        cv.convert(fullname_docx)
        cv.close()

        return fullname_docx

    @staticmethod
    def export_dispache_csv(header, rows, filename):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response, delimiter=';')
        writer.writerow(header)

        for row in rows:
            row_fields = [row.pk, row.contrat, row.get_statut_display()]
            writer.writerow(row_fields)

        response['Content-Disposition'] = "attachment; filename=%s.csv" % filename
        return response

    # Méhode générique pour télécharger un document.
    @staticmethod
    def download(request, pk, filename, name):
        filelocal = 'media/' + str(filename)
        file = open(filelocal)

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(filelocal))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + str(name) + '"'
        return response
