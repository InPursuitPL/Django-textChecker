from django import forms
from .models import StringText

class StringTextForm(forms.ModelForm):
    class Meta:
        model = StringText
        fields = ('text',)

class UploadFileForm(forms.Form):
    file = forms.FileField()

