import mimetypes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from core.constantes import CoreConstantes
from core.utils import ExportUtils, FileUtils

'''
Classe abstraite générique de gestion des exports : penser à définir get_content et get_filename
'''


class AbstractExportWebContentView(LoginRequiredMixin, View):
    template_name = None
    extension = None

    def get_context(self, request, *args, **kwargs):
        raise NotImplementedError('AbstractExportWebContentView : obligation de surcharger la méthode get_context()')

    def get_filename(self):
        raise NotImplementedError('AbstractExportWebContentView : obligation de surcharger la méthode get_filename()')

    def __get_extension(self):
        if self.extension is None:
            raise NotImplementedError('AbstractExportWebContentView : obligation de surcharger self.extension')
        return self.extension

    def __get_template_name(self):
        if self.template_name is None:
            raise NotImplementedError('AbstractExportWebContentView : obligation de renseigner le self.template_name')
        return self.template_name

    def get(self, request, *args, **kwargs):
        # Création du contenu HTML.
        html_content = render(request=request, template_name=self.__get_template_name(), context=self.get_context(request, *args, **kwargs)).content.decode()

        # Transformation du fichier.
        filepath = None
        if self.__get_extension() == CoreConstantes.Extension.PDF:
            filepath = ExportUtils.download_page_as_pdf_from_html(html_content)
        elif self.__get_extension() == CoreConstantes.Extension.DOCX:
            filepath = ExportUtils.download_page_as_docx_from_html(html_content)

        # Export du fichier.
        fileoutput_name = FileUtils.clean_filename('%s.%s' % (self.get_filename(), self.__get_extension().nom))
        with open(filepath, 'rb') as path:
            response = HttpResponse(path, content_type=self.__get_extension().content_type)
            response['Content-Disposition'] = "attachment; filename=%s" % fileoutput_name
            return response
