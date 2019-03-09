from django.contrib.auth.models import User
from django import forms
from cycles.models import Tenant, Cycle

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class CycleForm(forms.ModelForm):
    name = forms.CharField()
    endDate = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        model = Cycle
        fields = ('name', 'endDate', )

class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ('name', )
