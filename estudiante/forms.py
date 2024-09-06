from django import forms
from .models import ModelAnteproyecto, ModelProyectoFinal

#!funcionando
# class FormPrimeraSolicitud(forms.ModelForm):
#     class Meta:
#         model = ModelPrimeraSolicitud
#         fields = '__all__'


class FormAnteproyecto(forms.ModelForm):
    carta_presentacion_convert = forms.FileField(required=True)
    anteproyecto_convert = forms.FileField(required=True)

    class Meta:
        model = ModelAnteproyecto
        fields = ('nombre_anteproyecto', 'descripcion', 'nombre_integrante1', 'nombre_integrante2',
                  'carta_presentacion_convert', 'anteproyecto_convert', 'director', 'codirector')
        widgets = {
            'nombre_integrante2': forms.TextInput(attrs={'placeholder': 'Si tienes.'}),
            'codirector': forms.TextInput(attrs={'placeholder': 'Si tienes.'}),
        }

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        solicitud.nombre_anteproyecto = self.cleaned_data['nombre_anteproyecto']
        solicitud.nombre_integrante1 = self.cleaned_data['nombre_integrante1']
        solicitud.nombre_integrante2 = self.cleaned_data['nombre_integrante2']
        solicitud.descripcion = self.cleaned_data['descripcion']

        # Convierte los archivos en datos binarios y los asigna a los campos BinaryField
        solicitud.carta_presentacion = self.cleaned_data['carta_presentacion_convert'].read(
        )
        solicitud.anteproyecto = self.cleaned_data['anteproyecto_convert'].read(
        )

        solicitud.director = self.cleaned_data['director']
        solicitud.codirector = self.cleaned_data['codirector']

        if commit:
            solicitud.save()
        return solicitud

# formulario de proyecto final


class FormProyectoFinal(forms.ModelForm):
    doc_proyecto_final_form = forms.FileField(required=True)
    carta_presentacion_final_form = forms.FileField(required=True)

    class Meta:
        model = ModelProyectoFinal
        fields = ('doc_proyecto_final_form', 'carta_presentacion_final_form')

    def save(self, commit=True):
        form_proyecto_final = super().save(commit=False)
        form_proyecto_final.proyecto_final = self.cleaned_data['doc_proyecto_final_form'].read(
        )
        form_proyecto_final.carta_presentacion_final = self.cleaned_data[
            'carta_presentacion_final_form'].read()
        if commit:
            form_proyecto_final.save()
        return form_proyecto_final
