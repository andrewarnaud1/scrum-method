from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from core.forms.revolucy import HappyFamModelForm
from core.models import Utilisateur
# Formulaire de création d'un utilisateur pour la partie ADMIN.
from core.utils import UserUtils


class CreateUtilisateurAdminForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = '__all__'


# Formulaire de modification d'un utilisateur pour la partie ADMIN.
class EditUtilisateurAdminForm(forms.ModelForm):
    # Overide password pour afficher le message de réinitialisation.
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = Utilisateur
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditUtilisateurAdminForm, self).__init__(*args, **kwargs)

        # Gestion d'un group unique.
        pk_current_user = kwargs['instance'].pk
        user = Utilisateur.objects.get(id=pk_current_user)
        self.fields['groups'] = forms.ChoiceField(required=True, choices=[(g.id, g.name) for g in Group.objects.all()])
        if user.group is not None:
            self.initial['groups'] = user.group.id


# Formulaire d'authentification utilisateur avec recaptcha google.
class RecaptchaUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label="Email*", required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}), required=True)

    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Invisible(), required=True)

    def __init__(self, *args, **kwargs):
        super(RecaptchaUserLoginForm, self).__init__(*args, **kwargs)


# Formulaire de création d'un utilisateur pour la partie FRONT.
class CreateUtilisateurForm(HappyFamModelForm):
    select_fields = ['civilite']

    class Meta:
        model = Utilisateur
        fields = ('email', 'civilite', 'first_name', 'last_name', 'avatar', 'groups')

    def __init__(self, *args, **kwargs):
        super(CreateUtilisateurForm, self).__init__(*args, **kwargs)

        # Gestion d'un group unique.
        self.fields['groups'] = forms.ChoiceField(required=True, choices=[(g.id, g.name) for g in Group.objects.all()])
        self.fields['groups'].widget.attrs['class'] = 'form-control selectpicker'
        self.fields['groups'].widget.attrs['data-live-search'] = 'true'


# Formulaire de modification d'un utilisateur pour la partie FRONT.
class EditUtilisateurForm(HappyFamModelForm):
    select_fields = ['civilite']

    class Meta:
        model = Utilisateur
        fields = ('email', 'civilite', 'first_name', 'last_name', 'avatar', 'groups', 'is_active')

    def __init__(self, *args, **kwargs):
        super(EditUtilisateurForm, self).__init__(*args, **kwargs)

        # Gestion du rôle en fonction de l'utilisateur connecté.
        current_user = UserUtils.get_current_authenticated_user()
        if current_user.is_administrateur:

            # Gestion d'un group unique.
            self.fields['groups'] = forms.ChoiceField(required=True, choices=[(g.id, g.name) for g in Group.objects.all()])
            self.fields['groups'].widget.attrs['class'] = 'form-control selectpicker'
            self.fields['groups'].widget.attrs['data-live-search'] = 'true'

            if self.instance.group:
                self.initial['groups'] = self.instance.group.id
        else:
            del self.fields['groups']

        # Champs obligatoires.
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # Gestion spécifique du champ actif.
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'

    def clean(self):
        new_groups = self.cleaned_data.get('groups')
        group = Group.objects.get(pk=new_groups) if new_groups else self.instance.groups.first()

        # Toujours vérifier qu'il existe un administrateur actif.
        if group.name != Utilisateur.Role.ADMINISTRATEUR and \
                not Utilisateur.objects.exclude(pk=self.instance.pk).filter(is_active=True, is_staff=True, groups__name__exact=Utilisateur.Role.ADMINISTRATEUR).exists():
            raise forms.ValidationError('Attention, vous devez disposer au minimum d\'un administrateur actif')
