from django.contrib import admin
from dra import models
from dra import forms

class AccountAdmin(admin.ModelAdmin):
    form = forms.AccountForm

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Group)
admin.site.register(models.Repository)
admin.site.register(models.RepositoryPermissions)
