from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import models as authmodels
from django.contrib.auth.hashers import (
    check_password, make_password,
)

class Group(models.Model):
    """ Represents grouping of Accounts """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

class Account(models.Model):
    """ Represents a docker account """
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return '{}'.format(self.username)

class Repository(models.Model):
    """ Represents a repository prefix """
    name = models.CharField(max_length=100, unique=True)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Repositories'

    def __str__(self):
        return '{} [{}]'.format(self.name, 'public' if self.public else 'private')

class RepositoryPermissions(models.Model):
    """ Provides access to a repository for a group,
    possibly with write access """

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    write = models.BooleanField(default=False)

    class Meta:
        unique_together = (
                ('repository', 'group'),
                )

    def __str__(self):
        return '{}-{} [{}]'.format(self.repository, self.group, 'full' if self.write else 'read')
