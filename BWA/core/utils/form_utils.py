'''
Classe générique de gestion des formulaires : permet de valider un ensemble de formulaire, enregistrer un formset et faire la jointure avec une foreign key.
'''


class FormUtils:

    # Validation des formulaires.
    @staticmethod
    def are_forms_ok(**forms_to_valid):
        are_forms_ok = True

        # Parcours des formulaires.
        for name, form in forms_to_valid.items():

            # Formulaire de type Form ou ModelForm.
            if isinstance(form, (ModelForm, Form)) and not form.is_valid():
                are_forms_ok = False
                LogUtils.info(f'Formulaire {name} en erreur : {dict(form.errors.items())}')

            # Formset de formulaire.
            elif isinstance(form, BaseFormSet) and not form.is_valid():
                for error in form.errors:
                    if error.items():
                        are_forms_ok = False
                        LogUtils.info(f'Formset {name} en erreur : {dict(error.items())}')

        return are_forms_ok

    @staticmethod
    def save_formset(formset, **fields):

        # Instances à supprimer.
        form_instance_to_delete = []

        # Parcours des formulaires.
        for form in formset:
            form.is_valid()

            # Si le formulaire contient la checkbox DELETE, on supprime l'instance.
            if form.cleaned_data.get(CoreConstantes.Forms.FIELD_DELETE):
                if form.instance.pk:
                    form_instance_to_delete.append(form.instance)
                else:
                    continue

            # Sinon on sauvegarde l'objet et si le formulaire à été modifié.
            elif form.has_changed():
                form_instance = form.save(commit=False)
                # Mise à jour de la foreign_key.
                for name, value in fields.items():
                    setattr(form_instance, name, value)
                form_instance.save()

        # Suppression des instances.
        for form_instance in form_instance_to_delete: form_instance.delete()


from django.forms import BaseFormSet, Form, ModelForm, widgets

from core import CoreConstantes
from .log_utils import LogUtils

'''
Classe générique de gestion des formulaires : permet de valider un ensemble de formulaire, enregistrer un formset et faire la jointure avec une foreign key.
'''


class FormUtils:

    # Validation des formulaires.
    @staticmethod
    def are_forms_ok(**forms_to_valid):
        are_forms_ok = True

        # Parcours des formulaires.
        for name, form in forms_to_valid.items():

            # Formulaire de type Form ou ModelForm.
            if isinstance(form, (ModelForm, Form)) and not form.is_valid():
                are_forms_ok = False
                LogUtils.info(f'Formulaire {name} en erreur : {dict(form.errors.items())}')

            # Formset de formulaire.
            elif isinstance(form, BaseFormSet) and not form.is_valid():
                for error in form.errors:
                    if error.items():
                        are_forms_ok = False
                        LogUtils.info(f'Formset {name} en erreur : {dict(error.items())}')

        return are_forms_ok

    @staticmethod
    def save_formset(formset, **fields):

        # Instances à supprimer.
        form_instance_to_delete = []

        # Parcours des formulaires.
        for form in formset:
            form.is_valid()

            # Si le formulaire contient la checkbox DELETE, on supprime l'instance.
            if form.cleaned_data.get(CoreConstantes.Forms.FIELD_DELETE):
                if form.instance.pk:
                    form_instance_to_delete.append(form.instance)
                else:
                    continue

            # Sinon on sauvegarde l'objet et si le formulaire à été modifié.
            elif form.has_changed():
                form_instance = form.save(commit=False)
                # Mise à jour de la foreign_key.
                for name, value in fields.items():
                    setattr(form_instance, name, value)
                form_instance.save()

        # Suppression des instances.
        for form_instance in form_instance_to_delete: form_instance.delete()

    # Ajout des classes génériques aux différents composants du formulaire.
    @staticmethod
    def beautifier(fields, form_read_only=False, read_only_fields=[], select_fields=[], multi_select_fields=[], radiobutton_fields=[],
                   date_ddmmyyyy_fields=[], date_ddmm_fields=[], heure_hhmm_fields=[],
                   decimal2_fields=[], decimal4_fields=[], decimal6_fields=[],
                   pourcentage2_fields=[], pourcentage4_fields=[],
                   color_fields=[], checkbox_fields=[]):

        # Parcours des champs.
        for (name, field) in fields.items():
            field.widget.attrs['class'] = 'form-control'

            if name in select_fields:
                field.widget.attrs['class'] = 'form-control selectpicker'
                field.widget.attrs['data-live-search'] = 'true'

            if name in multi_select_fields:
                field.widget.attrs['class'] = 'form-control selectpicker'
                field.widget.attrs['multiple'] = 'multiple'
                field.widget.attrs['data-live-search'] = 'true'

            if name in radiobutton_fields:
                field.widget = widgets.RadioSelect({'class': 'form-control form-check-input'})

            if name in date_ddmmyyyy_fields:
                field.widget.attrs['class'] = 'form-control jqmask-date-ddmmyyyy'

            if name in date_ddmm_fields:
                field.widget.attrs['class'] = 'form-control jqmask-date-ddmm'

            if name in heure_hhmm_fields:
                field.widget.attrs['class'] = 'form-control jqmask-heure-hhmm'

            if name in decimal2_fields:
                field.widget = widgets.TextInput({'class': 'form-control autonum-decimal2'})

            if name in decimal4_fields:
                field.widget = widgets.TextInput({'class': 'form-control autonum-decimal4'})

            if name in decimal6_fields:
                field.widget = widgets.TextInput({'class': 'form-control autonum-decimal6'})

            if name in pourcentage2_fields:
                field.widget = widgets.TextInput({'class': 'form-control autonum-pourcent2'})

            if name in pourcentage4_fields:
                field.widget = widgets.TextInput({'class': 'form-control autonum-pourcent4'})

            if name in color_fields:
                field.widget.attrs['class'] = 'form-control form-control-color'

            if name in checkbox_fields:
                field.widget = widgets.CheckboxInput({'class': 'form-check'})

            if form_read_only or name in read_only_fields:
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = True
