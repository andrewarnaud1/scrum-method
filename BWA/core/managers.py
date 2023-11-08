from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models

from MGL.settings import NB_UTILISATEURS_MAX
from core.utils import EmailUtils, LogUtils
from core.utils import UserUtils


# Classe utilisée par la commande createuser et createsuperuser.
class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def nb_utilisateurs_max():
        return NB_UTILISATEURS_MAX

    def droit_ajout_utlisateur(self):
        return self.all().count() < UtilisateurManager.nb_utilisateurs_max()

    @staticmethod
    def droit_modifier_password(user_connected, user_to_edit):
        return bool(user_connected.is_administrateur or user_connected.pk == user_to_edit.pk)

    # Création ou mise à jour d'un utilisateur puis envoie du mail d'initialisation de mot de passe.
    def create_or_update_user_and_send_init_password_mail(self, old_email, email, group, **extra_fields):

        # Récupération de l'utilisateur courant.
        user_found_queryset = self.filter(email=old_email)

        # Pas de compte présent pour le moment, on créé l'utilisateur.
        if old_email is None or not user_found_queryset.exists():
            utilisateur = self.__create_or_update_user(pk=None, email=email, group=group, is_superuser=False, is_staff=False, **extra_fields)
            send_init_password_mail = True

        else:
            # Mise à jour de l'utilisateur identifié.
            utilisateur = self.__create_or_update_user(pk=user_found_queryset.first().pk, email=email, group=group, is_superuser=False, is_staff=False, **extra_fields)
            send_init_password_mail = False

        # Envoie du mail d'initialisation du mot de passe utilisateur.
        if send_init_password_mail:
            try:
                EmailUtils.send_init_password_mail(user=utilisateur)
            except Exception as e:
                LogUtils.error('Une erreur (%s) est survenue lors de l\'envoi d\'email d\'initialisation de mot de passe : %s' % (type(e).__name__, e))

        return utilisateur

    # Création ou mise à jour d'un utilisateur en fonction des paramètres courants.
    def __create_or_update_user(self, pk, email, group, is_superuser=False, is_staff=False, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        LogUtils.info("Création ou MAJ automatique de l'utilisateur %s" % email)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.pk = pk
        user.is_superuser = is_superuser
        user.is_staff = is_staff

        user.save(using=self._db)

        # Gestion des rôles.
        group_queryset = Group.objects.filter(name=group)
        if group and group_queryset.exists():
            user.groups.add(group_queryset.first())

        LogUtils.info("Utilisateur #%d enregistré" % user.pk)

        return user

    def _create_user_from_cmd(self, email, password, group, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Gestion des rôles.
        group_queryset = Group.objects.filter(name=group)
        if group and group_queryset.exists():
            user.groups.add(group_queryset.first())

        return user

    # Méthode de création d'un super utilisateur = administrateur.
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user_from_cmd(email, password, self.model.Role.ADMINISTRATEUR, **extra_fields)


class UtilisateurModelUserFilterManager(models.Manager):

    def get_queryset(self):
        current_user = UserUtils.get_current_authenticated_user()
        if current_user.is_administrateur:
            return super(UtilisateurModelUserFilterManager, self).get_queryset()
        return super(UtilisateurModelUserFilterManager, self).get_queryset().filter(pk=current_user.pk)


class UtilisateurUserFilterManager(models.Manager):

    def get_queryset(self):
        current_user = UserUtils.get_current_authenticated_user()
        if current_user.is_administrateur:
            return super(UtilisateurUserFilterManager, self).get_queryset()
        return super(UtilisateurUserFilterManager, self).get_queryset().filter(utilisateur=current_user)
