from django.db import models
from MGL.settings import MEDIA_URL
from core.models import Utilisateur, HappyFamModel


class Entreprise(HappyFamModel):
    raison_sociale = models.CharField(max_length=120)
    label = models.CharField(max_length=120, null=True, blank=True)
    siret = models.CharField(max_length=120)
    vat_intra = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = "entreprise"
        verbose_name_plural = "entreprises"

    def __str__(self):
        return self.raison_sociale

    @property
    def adresse_facturation(self):
        try:
            return Adresse.objects.filter(company=self, type='facturation').first()
        except Exception:
            return None

    @property
    def adresse_livraison(self):
        try:
            return Adresse.objects.filter(company=self, type='livraison').first()
        except Exception:
            return None


class Adresse(HappyFamModel):
    choix_adresse = [
        ('facturation', 'Facturation'),
        ('livraison', 'Livraison'),
    ]
    type = models.CharField(max_length=60, default='facturation', choices=choix_adresse)
    adresse = models.CharField(max_length=120)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=60)
    pays = models.CharField(max_length=60)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, null=True, blank=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "adresse"
        verbose_name_plural = "adresses"

    def __str__(self):
        return f'{self.adresse}, {self.code_postal} {self.ville} {self.pays}'
