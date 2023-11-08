from avis.models import Avis
from django import forms


class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = "__all__"
