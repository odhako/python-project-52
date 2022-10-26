from django.db import models
from django.utils.translation import pgettext as _


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)


class Status(TimeStampedModel):
    name = models.CharField(verbose_name=_('Status model field', 'Name'),
                            max_length=100,
                            unique=True,
                            null=False)
