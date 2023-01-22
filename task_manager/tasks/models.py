from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(TimeStampedModel):
    name = models.CharField(verbose_name=_('Name'),
                            max_length=100,
                            unique=True,
                            null=False)

    description = models.TextField(verbose_name=_('Description'),
                                   blank=True,
                                   null=True,)

    author = models.ForeignKey(User,
                               related_name='task_author',
                               verbose_name=_('Author'),
                               on_delete=models.RESTRICT)

    status = models.ForeignKey(Status,
                               verbose_name=_('Status'),
                               on_delete=models.RESTRICT)

    executor = models.ForeignKey(User,
                                 related_name='task_executor',
                                 verbose_name=_('Executor'),
                                 on_delete=models.RESTRICT,
                                 blank=True,
                                 null=True)

    labels = models.ManyToManyField(Label,
                                    blank=True,
                                    verbose_name=_('Labels'))

    def __str__(self):
        return self.name
