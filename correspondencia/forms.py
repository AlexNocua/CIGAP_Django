from django import forms
from .models import ModelRetroalimentacionesAnteproyecto


class FormRetroalimentacionAnteproyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(required=True)

    class Meta:
        model = ModelRetroalimentacionesAnteproyecto
        fields = ('retroalimentacion','doc_retroalimentacion_convert', 'estado')

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data['retroalimentacion']
        retroalimentacion.doc_retroalimentacion = self.cleaned_data['doc_retroalimentacion_convert'].read()
        retroalimentacion.estado = self.cleaned_data['estado']
        if commit:
            retroalimentacion.save()
        return retroalimentacion
