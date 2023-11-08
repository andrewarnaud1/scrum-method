from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _



class User(AbstractUser):
    RESTAURATEUR = 'restaurateur'
    CLIENT = 'client'
    ROLE_CHOICES = [
        (RESTAURATEUR, 'Restaurateur'),
        (CLIENT, 'Client'),
    ]

    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=CLIENT)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )


    def is_restaurateur(self):
        return self.role == self.RESTAURATEUR

    def is_client(self):
        return self.role == self.CLIENT

class RestaurateurProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Autres champs spécifiques au restaurateur

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Autres champs spécifiques au client
