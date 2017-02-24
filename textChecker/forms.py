from django import forms
from .models import StringText

class StringTextForm(forms.ModelForm):
    class Meta:
        model = StringText
        fields = ('text',)

# class StringTextForm(forms.Form):
#     text = forms.CharField()

class UploadFileForm(forms.Form):
    file = forms.FileField()

