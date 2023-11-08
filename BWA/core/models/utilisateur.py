from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from core.constantes import CoreConstantes
from core.managers import UtilisateurManager, UtilisateurModelUserFilterManager
from core.utils import FileUtils


# Classe utilisateur spécifique qui hérite de la classe User abstraite de django par défaut
# Cette classe permet de définir le champ identifiant unique par défaut
# Permet l'ajout d'attributs spécifiques
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    class Role:
        ADMINISTRATEUR = 'Administrateur'
        COMMERCIAL = 'Commercial'
        ADV = 'ADV'
        ACHAT = 'Achat'
        RH = 'RH'
        COMPTABLE = 'Comptable'
        CLIENT = 'Client'
        APPORTEUR = 'Apporteur'

        collaborateur_sans_droit_rh = [COMMERCIAL, ADV, ACHAT, COMPTABLE]
        collaborateur_avec_droit_rh = [ADMINISTRATEUR, RH]
        collaborateur = [ADMINISTRATEUR, ACHAT, ADV, COMMERCIAL, COMPTABLE, RH]

    # Attributs.
    email = models.EmailField('email address', unique=True)
    civilite = models.CharField(max_length=5, choices=CoreConstantes.Utilisateur.tuples_civilite, default=None, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to=FileUtils.generic_image_directory_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Définition de l'identifiant unique de l'utilisateur.
    USERNAME_FIELD = 'email'

    # Liste des champs obligatoires lors de la création d'un utilisateur par commande de gestion.
    REQUIRED_FIELDS = []

    objects = UtilisateurManager()
    user_filter = UtilisateurModelUserFilterManager()

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ['is_active', 'last_name', 'first_name']

    def __str__(self):
        return self.full_name

    def has_group_perms(self, permissions):
        return all(perm in self.get_group_permissions() for perm in permissions)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def object_name(self):
        return f'l\'utilisateur {self.full_name} avec l\'email {self.email}'

    @property
    def group(self):
        for group in self.groups.all():
            return group
        return None

    @property
    def is_deletable(self):
        return not hasattr(self, 'collaborateur') and not hasattr(self, 'apporteur') and not hasattr(self, 'client')

    @property
    def is_administrateur(self):
        return self.groups.filter(name=Utilisateur.Role.ADMINISTRATEUR).exists()

    @property
    def is_commercial(self):
        return self.groups.filter(name=Utilisateur.Role.COMMERCIAL).exists()

    @property
    def is_adv(self):
        return self.groups.filter(name=Utilisateur.Role.ADV).exists()

    @property
    def is_achat(self):
        return self.groups.filter(name=Utilisateur.Role.ACHAT).exists()

    @property
    def is_compta(self):
        return self.groups.filter(name=Utilisateur.Role.COMPTABLE).exists()

    @property
    def is_rh(self):
        return self.groups.filter(name=Utilisateur.Role.RH).exists()

    @property
    def is_collaborateur_sans_droit_rh(self):
        return self.groups.filter(name__in=Utilisateur.Role.collaborateur_sans_droit_rh).exists()

    @property
    def is_collaborateur_avec_droit_rh(self):
        return self.groups.filter(name__in=Utilisateur.Role.collaborateur_avec_droit_rh).exists()

    # Rôles externes.
    @property
    def is_client(self):
        return self.groups.filter(name=Utilisateur.Role.CLIENT).exists()

    @property
    def is_apporteur(self):
        return self.groups.filter(name=Utilisateur.Role.APPORTEUR).exists()
