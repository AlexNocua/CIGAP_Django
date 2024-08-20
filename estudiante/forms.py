from django import forms
from .models import ModelPrimeraSolicitud

#!funcionando
class FormPrimeraSolicitud(forms.ModelForm):
    class Meta:
        model = ModelPrimeraSolicitud
        fields = '__all__'
