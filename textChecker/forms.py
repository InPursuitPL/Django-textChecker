import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class StringTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Tekst')


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Plik')



class WrongWordForm(forms.Form):
    word = forms.CharField(label='Słowo lub wyrażenie')


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Hasło',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Hasło (ponownie)',
                        widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Hasła nie były te same.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Nazwa użytkownika może zawierać tylko'
                                        'litery oraz znak podkreślenia.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Nazwa użytkownika jest już zajęta.', code='invalid')