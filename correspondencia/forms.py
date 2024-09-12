from django import forms
from .models import ModelRetroalimentaciones, ModelSolicitudes, ModelAsignacionJurados


class FormRetroalimentacionAnteproyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(required=True)

    class Meta:
        model = ModelRetroalimentaciones
        fields = ('retroalimentacion',
                  'doc_retroalimentacion_convert', 'estado')

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data['retroalimentacion']
        retroalimentacion.doc_retroalimentacion = self.cleaned_data['doc_retroalimentacion_convert'].read(
        )
        retroalimentacion.estado = self.cleaned_data['estado']
        if commit:
            retroalimentacion.save()
        return retroalimentacion


class FormRetroalimentacionProyecto(forms.ModelForm):
    doc_retroalimentacion_convert = forms.FileField(required=True)

    class Meta:
        model = ModelRetroalimentaciones
        fields = ('retroalimentacion',
                  'doc_retroalimentacion_convert', 'estado')

    def save(self, commit=True):
        retroalimentacion = super().save(commit=False)
        retroalimentacion.retroalimentacion = self.cleaned_data['retroalimentacion']
        retroalimentacion.doc_retroalimentacion = self.cleaned_data['doc_retroalimentacion_convert'].read(
        )
        retroalimentacion.estado = self.cleaned_data['estado']
        if commit:
            retroalimentacion.save()
        return retroalimentacion


# creacion del modelo de solicitudes
class FormSolicitudes(forms.ModelForm):
    documento_soporte_convert = forms.FileField(required=True)

    class Meta:
        model = ModelSolicitudes
        fields = [
            'relacionado_con',
            'retroalimentaciones',
            'tipo_solicitud',
            'motivo_solicitud',
            'documento_soporte_convert',
        ]

    def __init__(self, *args, **kwargs):
        super(FormSolicitudes, self).__init__(*args, **kwargs)
        # Hacer que los campos específicos sean requeridos
        self.fields['relacionado_con'].required = True
        self.fields['motivo_solicitud'].required = True
        self.fields['documento_soporte_convert'].required = True

    def save(self, commit=False):
        solicitudes = super().save(commit=True)
        solicitudes.relacionado_con = self.cleaned_data['relacionado_con']
        solicitudes.tipo_solicitud = self.cleaned_data['tipo_solicitud']
        solicitudes.motivo_solicitud = self.cleaned_data['motivo_solicitud']
        solicitudes.documento_soporte = self.cleaned_data['documento_soporte_convert'].read(
        )
        if commit:
            solicitudes.save()
        return solicitudes

# formulario de asignacion de jurados


class FormJurados(forms.ModelForm):
    nombre_jurado = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ModelAsignacionJurados
        fields = [

            'nombre_jurado',

        ]

    def save(self, commit=False):
        jurados = super().save(commit=True)
        if commit:
            jurados.save()
        return jurados
