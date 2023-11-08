from django import forms

from core.utils.form_utils import FormUtils


# HappyFamModelForm générique qui hérite de ModelForm et qui permet de mettre en forme le formulaire.
class HappyFamModelForm(forms.ModelForm):
    form_read_only = False
    read_only_fields = []
    select_fields = []
    multi_select_fields = []
    date_ddmmyyyy_fields = []
    date_ddmm_fields = []
    heure_hhmm_fields = []
    decimal2_fields = []
    decimal4_fields = []
    decimal6_fields = []
    pourcentage2_fields = []
    pourcentage4_fields = []
    color_fields = []
    checkbox_fields = []

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(HappyFamModelForm, self).__init__(*args, **kwargs)

        FormUtils.beautifier(fields=self.fields, form_read_only=self.form_read_only, read_only_fields=self.read_only_fields,
                             select_fields=self.select_fields, multi_select_fields=self.multi_select_fields,
                             date_ddmmyyyy_fields=self.date_ddmmyyyy_fields, date_ddmm_fields=self.date_ddmm_fields, heure_hhmm_fields=self.heure_hhmm_fields,
                             decimal2_fields=self.decimal2_fields, decimal4_fields=self.decimal4_fields, decimal6_fields=self.decimal6_fields,
                             pourcentage2_fields=self.pourcentage2_fields, pourcentage4_fields=self.pourcentage4_fields,
                             color_fields=self.color_fields, checkbox_fields=self.checkbox_fields)


# HappyFamForm générique qui hérite de Form et qui permet de mettre en forme le formulaire.
class HappyFamForm(forms.Form):
    form_read_only = False
    read_only_fields = []
    select_fields = []
    multi_select_fields = []
    date_ddmmyyyy_fields = []
    date_ddmm_fields = []
    heure_hhmm_fields = []
    decimal2_fields = []
    decimal4_fields = []
    decimal6_fields = []
    pourcentage2_fields = []
    pourcentage4_fields = []
    color_fields = []
    checkbox_fields = []

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(HappyFamForm, self).__init__(*args, **kwargs)

        FormUtils.beautifier(fields=self.fields, form_read_only=self.form_read_only, read_only_fields=self.read_only_fields,
                             select_fields=self.select_fields, multi_select_fields=self.multi_select_fields,
                             date_ddmmyyyy_fields=self.date_ddmmyyyy_fields, date_ddmm_fields=self.date_ddmm_fields, heure_hhmm_fields=self.heure_hhmm_fields,
                             decimal2_fields=self.decimal2_fields, decimal4_fields=self.decimal4_fields, decimal6_fields=self.decimal6_fields,
                             pourcentage2_fields=self.pourcentage2_fields, pourcentage4_fields=self.pourcentage4_fields,
                             color_fields=self.color_fields, checkbox_fields=self.checkbox_fields)
