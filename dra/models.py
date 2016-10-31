from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import models as authmodels

class Repository(models.Model):
    """ Represents a single repository """
    name = models.CharField(max_length=100)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Repositories'

    def __str__(self):
        return '{0} [{1}]'.format(self.name, 'public' if self.public else 'private')

class RepositoryPermissions(models.Model):
    """ Provides access to a repository for a group,
    possibly with write access """

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    sgroup = models.ForeignKey(authmodels.Group, on_delete=models.CASCADE)
    write = models.BooleanField(default=False)

    class Meta:
        unique_together = (
                ('repository', 'sgroup'),
                )

    def __str__(self):
        return '{0}-{1} [{2}]'.format(self.repository, self.sgroup, 'full' if self.write else 'read')
