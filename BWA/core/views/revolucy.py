from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView

from core.utils import LogUtils

'''
Classe générique de suppression d'un objet.
L'objet doit disposer de la property object_name pour qualifier le nom de l'objet.
'''


class HappyFamDeleteView(DeleteView):

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk
        success_message = self.success_message()
        if self.get_form().is_valid():
            try:
                self.object.delete()
                LogUtils.info(f'{self.model._meta.verbose_name.capitalize()} #{pk} supprimée avec succès')
                messages.add_message(request, messages.INFO, message=success_message)
            except ProtectedError as e:
                LogUtils.info(f'{self.model._meta.verbose_name.capitalize()} #{self.object.pk} {e}')
                messages.add_message(request, messages.ERROR, message=f"Impossible de supprimer {self.object.object_name}, l'objet est toujours référencé.")
            except Exception as e:
                LogUtils.error(f"Une erreur ({type(e).__name__}) est survenue à la suppression de {self.object.object_name} #{self.object.pk}: {e}")
                messages.add_message(request, messages.ERROR, message=f"Une erreur est survenue à la suppression de {self.object.object_name}")

        return HttpResponseRedirect(self.get_success_url())
