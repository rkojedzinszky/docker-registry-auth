from django.forms import ModelForm, PasswordInput
from dra.models import Account

class AccountForm(ModelForm):
    class Meta:
        fields = ('username', 'password', 'groups')
        model = Account
        widgets = {
                'password': PasswordInput,
                }

    def save(self, commit=True):
        account = super(AccountForm, self).save(commit=False)
        account.set_password(self.cleaned_data['password'])
        if commit:
            account.save()
        return account
