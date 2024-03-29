from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel


class Label(TimeStampedModel):
    name = models.CharField(verbose_name=_('Name'),
                            max_length=100,
                            unique=True,
                            null=False)

    def __str__(self):
        return self.name
