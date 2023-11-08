from django.db import models

from core.models import CurrentUserField
from core.utils import DateUtils


class HappyFamModel(models.Model):
    created_user = CurrentUserField(on_insert=True)
    created_date = models.DateTimeField(auto_now_add=DateUtils.now())
    updated_user = CurrentUserField(on_update=True)
    updated_date = models.DateTimeField(auto_now=DateUtils.now())

    class Meta:
        abstract = True
        ordering = ['-created_date']
