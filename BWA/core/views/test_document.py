from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseNotFound
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView

from MGL.settings import URL_PROTOCOL, URL_DOMAIN
from achat.models import FactureAchat, BCAchat
from affaire_negoce.models import AffaireNegoce, FournisseurAffaire, ProduitAffaire, Chargement
from affaire_negoce.utils import PFAchatUtils
from core.utils import UserUtils
from ventes.models import FactureVente

'''
Classe d'affichage d'un email pour test.
'''


class HappyFamTestDocumentView(LoginRequiredMixin, TemplateView):
    template_name = 'tableau_bord/tbd.html'

    def get_template_names(self):
        document_folder = self.kwargs.get('document_folder')
        document_name = self.kwargs.get('document_name')
        return [f'document/{document_folder}/{document_name}']

    def get_context_data(self, **kwargs):
        context = super(HappyFamTestDocumentView, self).get_context_data(**kwargs)

        # Vérification utilisateur.
        current_user = UserUtils.get_current_authenticated_user()
        if not current_user.is_administrateur:
            return HttpResponseNotFound()

        # Context générique.
        context['URL_BASE'] = f'{URL_PROTOCOL}://{URL_DOMAIN}'
        context['uidb64'] = urlsafe_base64_encode(force_bytes(current_user.pk))
        context['token'] = default_token_generator.make_token(current_user)

        # Context spécifique.
        self.add_custom_context(context)

        return context

    def add_custom_context(self, context):

        # Ajout d'une potentielle affaire.
        id_affaire_negoce = self.request.GET.get('id_affaire_negoce', None)
        if id_affaire_negoce:
            context['affaire_negoce'] = AffaireNegoce.objects.get(pk=id_affaire_negoce)

        # Ajout d'une potentielle facture de vente.
        id_facture_vente = self.request.GET.get('id_facture_vente', None)
        if id_facture_vente:
            context['facture_vente'] = FactureVente.objects.get(pk=id_facture_vente)

        # Ajout d'une potentielle facture d'achat.
        id_facture_achat = self.request.GET.get('id_facture_achat', None)
        if id_facture_achat:
            context['facture_achat'] = FactureAchat.objects.get(pk=id_facture_achat)

        # Ajout d'un potentiel chargement.
        id_chargement = self.request.GET.get('id_chargement', None)
        if id_chargement:
            context['chargement'] = Chargement.objects.get(pk=id_chargement)

        # Ajout d'un potentiel bc achat.
        id_bc_achat = self.request.GET.get('id_bc_achat', None)
        if id_bc_achat:
            bc_achat = BCAchat.objects.get(pk=id_bc_achat)

            _, total_montant_ht, total_montant_ttc = PFAchatUtils.total_montant_ht_net(
                bc_achat.fournisseur_affaire)

            total_montant_tva = total_montant_ttc - total_montant_ht

            context['bc_achat'] = bc_achat
            context['total_montant_ht'] = total_montant_ht
            context['total_montant_ttc'] = total_montant_ttc
            context['total_montant_tva'] = total_montant_tva

        # Ajout d'une potentielle affaire.
        id_fournisseur_affaire = self.request.GET.get('id_fournisseur_affaire', None)
        if id_fournisseur_affaire:
            # Récupération du fournisseur affaire.
            fournisseur_affaire = FournisseurAffaire.objects.get(pk=id_fournisseur_affaire)
            produits_affaire = ProduitAffaire.objects.filter(affaire_negoce=fournisseur_affaire.affaire_negoce,
                                                             produit__fournisseur=fournisseur_affaire.fournisseur)

            _, total_montant_ht, total_montant_ttc = PFAchatUtils.total_montant_ht_net(
                fournisseur_affaire)

            total_montant_tva = total_montant_ttc - total_montant_ht

            context['fournisseur_affaire'] = fournisseur_affaire
            context['produits_affaire'] = produits_affaire
            context['total_montant_ht'] = total_montant_ht
            context['total_montant_ttc'] = total_montant_ttc
            context['total_montant_tva'] = total_montant_tva

        # Ajout de produits de chargement pour un fournisseur pour un chargement
        if id_chargement and id_fournisseur_affaire:
            fournisseur_affaire = FournisseurAffaire.objects.get(pk=id_fournisseur_affaire)
            chargement_fournisseur = fournisseur_affaire.affaire_negoce.chargement_set.get(pk=id_chargement)

            context['chargement_fournisseur'] = chargement_fournisseur
