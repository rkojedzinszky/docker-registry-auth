from django.forms import ModelForm, CharField, PasswordInput
from dra.models import Account

class AccountForm(ModelForm):
    npassword = CharField(max_length=100, label='New password', required=False, widget=PasswordInput)

    class Meta:
        fields = ('username', 'npassword', 'groups', 'requests')
        readonly = ('requests',)
        model = Account

    def save(self, commit=True):
        account = super(AccountForm, self).save(commit=False)
        password = self.cleaned_data['npassword']
        if password != '':
            account.set_password(password)
        if commit:
            account.save()
        return account
