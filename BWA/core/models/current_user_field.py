import warnings
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import UserUtils


class CurrentUserField(models.CharField):
    warning = ("You passed an argument to CurrentUserField that will be "
               "ignored. Avoid args and following kwargs: default, null, to.")
    description = _(
        'as default value sets the current logged in user if available')
    defaults = dict(max_length=200, null=True)

    def __init__(self, *args, **kwargs):
        self.on_insert = kwargs.pop("on_insert", False)
        self.on_update = kwargs.pop("on_update", False)

        if self.on_insert or self.on_update:
            kwargs["editable"] = False
            kwargs["blank"] = True

        if "default" not in kwargs:
            kwargs["default"] = UserUtils.get_current_authenticated_user_email()

        kwargs.update(self.defaults)
        super(CurrentUserField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CurrentUserField, self).deconstruct()
        if self.on_update:
            kwargs['on_update'] = self.on_update
            del kwargs['editable']
            del kwargs["blank"]

        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if (self.on_insert and model_instance.pk) is None or self.on_update:
            value = UserUtils.get_current_authenticated_user_email()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(CurrentUserField, self).pre_save(model_instance, add)
