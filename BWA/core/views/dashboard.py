from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.views.breadcrumb_mixin import HappyFamBreadcrumbMixin
from core.utils import PythonUtils, UserUtils
from gestion.models import Tache


class DashboardView(LoginRequiredMixin, HappyFamBreadcrumbMixin, TemplateView):
    template_name = 'index.html'

    def get_breadcrumb(self, **kwargs):
        return [
            ('Tableau de bord', reverse_lazy('dashboard')),
        ]

    def get_context_data(self, form=None, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['taches'] = Tache.user_filter.filter(utilisateur=UserUtils.get_current_authenticated_user())
        return context


class DeleteObjectView(LoginRequiredMixin, TemplateView):
    permissions = []

    def get(self, request, *args, **kwargs):
        return_url = request.GET.get('return_url')
        module_name = request.GET.get('module_name')
        class_name = request.GET.get('class_name')
        if not return_url:
            raise BadRequest()
        if not module_name:
            messages.add_message(request, messages.ERROR,
                                 message='Veuillez renseigner le paramètre "module_name" dans l\'url')
        if not class_name:
            messages.add_message(request, messages.ERROR,
                                 message='Veuillez renseigner le paramètre "class_name" dans l\'url')
            return HttpResponseRedirect(redirect_to=return_url)

        instance = get_object_or_404(PythonUtils.class_for_name('%s.models' % module_name, class_name),
                                     pk=kwargs.get('pk'))
        try:
            instance.delete()
            messages.add_message(request, messages.INFO, message='Suppression effectuée avec succès')
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 message='Erreur (%s) est survenue lors de la suppression %s' % (type(e).__name__, e))
        return HttpResponseRedirect(redirect_to=return_url)
