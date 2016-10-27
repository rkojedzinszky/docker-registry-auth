from django.contrib import admin
from dra import models

admin.site.register(models.Repository)
admin.site.register(models.RepositoryPermissions)
