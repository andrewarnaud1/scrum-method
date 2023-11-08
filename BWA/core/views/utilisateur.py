from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from core.forms import CreateUtilisateurForm, EditUtilisateurForm
from core.forms.utilisateur import RecaptchaUserLoginForm
from core.models import Utilisateur
from core.utils import EmailUtils, FormUtils, LogUtils
from core.views import HappyFamDeleteView
from core.views.breadcrumb_mixin import HappyFamBreadcrumbMixin

'''
Classe de gestion des utilisateurs : listing, création, modification, authentification, reset password, ...
'''


class ListUtilisateurView(HappyFamBreadcrumbMixin, TemplateView):
    template_name = 'core/utilisateur-gestion.html'

    # Gestion du fil d'arianne.
    def get_breadcrumb(self, **kwargs):
        return [
            ('Tableau de bord', reverse_lazy('dashboard')),
            ('Utilisateurs', reverse_lazy('core:liste-utilisateur')),
        ]

    def get_context_data(self, *args, **kwargs):
        context = super(ListUtilisateurView, self).get_context_data(**kwargs)
        context['nb_utilisateurs_actif'] = Utilisateur.objects.filter(is_active=True).count()
        context['nb_utilisateurs_inactif'] = Utilisateur.objects.filter(is_active=False).count()
        context['nb_administrateurs'] = Utilisateur.objects.filter(groups__name=Utilisateur.Role.ADMINISTRATEUR).count()
        context['utilisateurs'] = Utilisateur.objects.all()
        context['droit_ajouter_utilisateur'] = Utilisateur.objects.droit_ajout_utlisateur()
        return context


class CreateUtilisateurView(LoginRequiredMixin, HappyFamBreadcrumbMixin, TemplateView):
    template_name = 'core/utilisateur-nouveau.html'
    utilisateur_form_class = CreateUtilisateurForm

    # Gestion du fil d'arianne.
    def get_breadcrumb(self, **kwargs):
        return [
            ('Tableau de bord', reverse_lazy('dashboard')),
            ('Utilisateurs', reverse_lazy('core:liste-utilisateur')),
            (f'Création d\'un utilisateur', ''),
        ]

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)

        # Redirection vers la liste des utilisateurs si le nombre d'utilisateurs max a été atteint.
        if not Utilisateur.objects.droit_ajout_utlisateur():
            LogUtils.info(f"Impossible de créer un nouvel utilisateur, le nombre d'utilisateurs max a été atteint : {Utilisateur.objects.nb_utilisateurs_max()}")
            return HttpResponseRedirect(reverse('core:liste-utilisateur'))

        return response

    def get_context_data(self, utilisateur_form=None, **kwargs):
        context = super(CreateUtilisateurView, self).get_context_data(**kwargs)
        context['form'] = utilisateur_form or self.utilisateur_form_class()
        return context

    def post(self, request, **kwargs):
        LogUtils.info("Demande de création d'un utilisateur")

        # Récupération du formulaire et du context.
        utilisateur_form = self.utilisateur_form_class(data=request.POST, files=request.FILES)
        context = self.get_context_data(utilisateur_form=utilisateur_form, **kwargs)

        # Validation du formulaire.
        if not FormUtils.are_forms_ok(utilisateur_form=utilisateur_form):
            return self.render_to_response(context, status=400)

        # Sauvegarde de l'utilisateur.
        try:
            with transaction.atomic():
                utilisateur = utilisateur_form.save()

        except Exception as e:
            LogUtils.error(f'Une erreur ({type(e).__name__}) est survenue à la création de l\'utilisateur : {e}')
            messages.add_message(request, messages.ERROR, message="Une erreur est survenue lors de la création de l\'utilisateur")
            return self.render_to_response(context, status=400)

        # Envoi du mail d'initialisation de mot de passe.
        try:
            EmailUtils.send_init_password_mail(utilisateur)
        except Exception as e:
            LogUtils.error(f"Une erreur ({type(e).__name__}) est survenue à l'envoi du mail d'initialisation de mot de passe : {e}")
            messages.add_message(request, messages.ERROR, message=f"Impossible d'envoyer le mail d'initialisation de mot de passe : merci de contacter votre administrateur !")

        # Redirection vers l'utilisateur en mode modification
        _msg = f'Utilisateur {utilisateur.full_name} créé avec succès'
        messages.add_message(request, messages.INFO, message=_msg)
        return HttpResponseRedirect(reverse('core:liste-utilisateur'))


class EditUtilisateurView(HappyFamBreadcrumbMixin, TemplateView):
    template_name = 'core/utilisateur-modification.html'
    utilisateur_form_class = EditUtilisateurForm

    # Gestion du fil d'arianne.
    def get_breadcrumb(self, **kwargs):
        if self.request.user.is_administrateur:
            return [
                ('Tableau de bord', reverse_lazy('dashboard')),
                ('Utilisateurs', reverse_lazy('core:liste-utilisateur')),
                ('Édition de mon profil', ''),
            ]
        return [
            ('Tableau de bord', reverse_lazy('dashboard')),
            ('Édition de mon profil', ''),
        ]

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        user = get_object_or_404(Utilisateur, pk=kwargs.get('pk'))

        # Redirection vers la modification de l'utilisateur si non admin
        if user != self.request.user and not self.request.user.is_administrateur:
            LogUtils.info("Impossible d'accéder à la modification d'un autre utilisateur")
            return HttpResponseRedirect(reverse('core:modification-utilisateur', args=[self.request.user.pk]))

        return response

    # Identification du formulaire de modification de mot de passe.
    def get_update_passsword_form(self, user_connected: Utilisateur, user_to_edit: Utilisateur, data=None):
        change_password_form_class = SetPasswordForm if user_connected.is_administrateur and user_connected != user_to_edit else PasswordChangeForm
        return change_password_form_class(user=user_to_edit, data=data)

    def get_context_data(self, utilisateur_form=None, password_form=None, *args, **kwargs):
        # Récupération de l'utilisateur.
        user_to_edit = get_object_or_404(Utilisateur, pk=kwargs.get('pk'))

        # Initialisation du context et des formulaires.
        context = super(EditUtilisateurView, self).get_context_data(**kwargs)
        context['utilisateur_form'] = utilisateur_form or self.utilisateur_form_class(instance=user_to_edit)

        # Configuration du formulaire de moditication de mot de passe.
        context['droit_modifier_password'] = Utilisateur.objects.droit_modifier_password(user_connected=self.request.user, user_to_edit=user_to_edit)
        context['password_form'] = password_form or self.get_update_passsword_form(user_connected=self.request.user, user_to_edit=user_to_edit)
        context['afficher_current_password'] = (context['password_form'].__class__.__name__ != SetPasswordForm.__name__)

        # Refresh forcé de l'utilisateur pour prise en compte direct après modification.
        context['user'] = get_user(self.request)

        return context

    def post(self, request, **kwargs):
        # Récupération de l'utilisateur.
        if kwargs.get('pk'):
            user_to_edit = get_object_or_404(Utilisateur, pk=kwargs.get('pk'))

        # Modification du mot de passe utilisateur.
        if 'change-password-submit' in request.POST:
            return self.update_password(request=request, user_to_edit=user_to_edit, **kwargs)

        LogUtils.info("Demande de modification de l'utilisateur #%d %s" % (user_to_edit.pk, user_to_edit.email))

        # Récupération du formulaire et du context.
        utilisateur_form = self.utilisateur_form_class(data=request.POST, files=request.FILES, instance=user_to_edit)
        context = self.get_context_data(utilisateur_form=utilisateur_form, **kwargs)

        # Validation du formulaire.
        if not FormUtils.are_forms_ok(utilisateur_form=utilisateur_form):
            return self.render_to_response(context, status=400)

        # Modification de l'utilisateur.
        try:
            with transaction.atomic():
                utilisateur = utilisateur_form.save()

        except Exception as e:
            LogUtils.error(f"Une erreur ({type(e).__name__}) est survenue à la mise à jour de l'utilisateur : {e}")
            messages.add_message(request, messages.ERROR, message="Une erreur est survenue à la mise à jour de l'utilisateur")
            return self.render_to_response(context, status=400)

        msg = f'Compte utilisateur {utilisateur.email} mis à jour avec succès'
        LogUtils.info(msg)
        messages.add_message(request, messages.INFO, message=msg)
        return self.render_to_response(self.get_context_data(**kwargs), status=200)

    def update_password(self, request, user_to_edit, **kwargs):
        LogUtils.info(f'Demande de modification de mot de passe du compte [{user_to_edit.email}]')

        # Récupération du formulaire et du context.
        password_form = self.get_update_passsword_form(user_connected=self.request.user, user_to_edit=user_to_edit, data=request.POST)
        context = self.get_context_data(password_form=password_form, **kwargs)

        # Validation du formulaire.
        if not FormUtils.are_forms_ok(password_form=password_form):
            return self.render_to_response(context, status=400)

        # Mise à jour du mot de passe.
        try:
            # Unique transaction.
            with transaction.atomic():
                utilisateur = password_form.save()
                update_session_auth_hash(request, utilisateur)

        except Exception as e:
            LogUtils.error(f'Une erreur ({type(e).__name__}) est survenue à la mise à jour du mot de passe utilisateur : {e}')
            messages.add_message(request, messages.ERROR, message="Une erreur est survenue à la mise à jour du mot de passe utilisateur")
            return self.render_to_response(context, status=400)

        context = self.get_context_data(**kwargs)
        LogUtils.info(f'Mise à jour de mot de passe du compte {user_to_edit.email} OK')
        messages.add_message(request, messages.INFO, message='Mot de passe utilisateur mis à jour avec succès')
        return self.render_to_response(context, status=200)


class RecaptchaUserLoginView(TemplateView):
    template_name = 'connexion.html'
    user_login_form_class = RecaptchaUserLoginForm

    def get_context_data(self, login_form=None, *args, **kwargs):
        context = super(RecaptchaUserLoginView, self).get_context_data(**kwargs)
        context['login_form'] = login_form or self.user_login_form_class()
        return context

    def post(self, request, *args, **kwargs):

        # Récupération et validation du formulaire.
        login_form = self.user_login_form_class(request=request, data=request.POST)
        if not login_form.is_valid():
            LogUtils.info('Formulaire d\'authentification en erreur : %s' % dict(login_form.errors.items()))
            context = self.get_context_data(login_form=login_form, **kwargs)
            return self.render_to_response(context=context, status=403)

        # Tentative d'authentification de l'utilisateur.
        user = authenticate(username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
        if user is not None:
            login(request, user)
            LogUtils.info('Authentification de l\'utilisateur OK')
            return HttpResponseRedirect(reverse('dashboard'))

        LogUtils.info('Authentification incorrect : utilisateur ou mot de passe invalide')
        return self.render_to_response(context=self.get_context_data(), status=403)


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'core/password_reset.html'

    def form_valid(self, form):
        self.email = form.cleaned_data['email']
        try:
            # Récupération de l'utilisateur depuis son identifiant.
            utiliseur_trouve = Utilisateur.objects.get(email=self.email)
            EmailUtils.send_init_password_mail(utiliseur_trouve)
        except Utilisateur.DoesNotExist:
            pass
        except Exception as e:
            LogUtils.error("Erreur à l'envoi du mail de réinitialisation de mot de passe")
            pass

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('password_reset_done', kwargs={'email': self.email})


'''
Classe de suppression d'un utilisateur.
'''


class DeleteUtilisateurView(LoginRequiredMixin, HappyFamDeleteView):
    model = Utilisateur
    success_url = reverse_lazy('core:liste-utilisateur')

    def success_message(self):
        return f'{self.model._meta.verbose_name.capitalize()} supprimé avec succès.'
