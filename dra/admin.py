from django.contrib import admin
from dra import models
from dra import forms

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    form = forms.AccountForm
    ordering = ('username',)
    list_display = ('username',)
    list_filter = ('groups',)

@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'public')
    list_filter = ('public',)

@admin.register(models.RepositoryPermissions)
class RepositoryPermissionsAdmin(admin.ModelAdmin):
    ordering = ('repository', 'group')
    list_display = ('repository', 'group', 'write')
    list_filter = ('repository', 'group')
