from django import forms
from .models import ModelAnteproyecto, ModelProyectoFinal, ModelObjetivoGeneral, ModelObjetivosEspecificos, ModelActividades

#!funcionando
# class FormPrimeraSolicitud(forms.ModelForm):
#     class Meta:
#         model = ModelPrimeraSolicitud
#         fields = '__all__'


class FormAnteproyecto(forms.ModelForm):
    carta_presentacion_convert = forms.FileField(required=False)
    anteproyecto_convert = forms.FileField(required=False)

    class Meta:
        model = ModelAnteproyecto
        fields = ('nombre_anteproyecto', 'descripcion', 'nombre_integrante1', 'nombre_integrante2',
                  'carta_presentacion_convert', 'anteproyecto_convert', 'director', 'codirector')
        widgets = {
            'nombre_integrante2': forms.TextInput(attrs={'placeholder': 'Si tienes.'}),
            'codirector': forms.TextInput(attrs={'placeholder': 'Si tienes.'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormAnteproyecto, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si el anteproyecto ya existe (es una actualización), haz opcional el campo
            self.fields['nombre_anteproyecto'].required = False

    def save(self, commit=True):
        solicitud = super().save(commit=False)
        solicitud.nombre_anteproyecto = self.cleaned_data.get(
            'nombre_anteproyecto', solicitud.nombre_anteproyecto)
        solicitud.nombre_integrante1 = self.cleaned_data.get(
            'nombre_integrante1', solicitud.nombre_integrante1)
        solicitud.nombre_integrante2 = self.cleaned_data.get(
            'nombre_integrante2', solicitud.nombre_integrante2)
        solicitud.descripcion = self.cleaned_data.get(
            'descripcion', solicitud.descripcion)

        # Solo reemplaza los archivos si se han proporcionado nuevos
        if self.cleaned_data.get('carta_presentacion_convert'):
            solicitud.carta_presentacion = self.cleaned_data['carta_presentacion_convert'].read(
            )

        if self.cleaned_data.get('anteproyecto_convert'):
            solicitud.anteproyecto = self.cleaned_data['anteproyecto_convert'].read(
            )

        solicitud.director = self.cleaned_data.get(
            'director', solicitud.director)
        solicitud.codirector = self.cleaned_data.get(
            'codirector', solicitud.codirector)

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

        # Leer los archivos como binarios y agregar mensajes de depuración
        doc_proyecto_final = self.cleaned_data['doc_proyecto_final_form'].read(
        )
        carta_presentacion_final = self.cleaned_data['carta_presentacion_final_form'].read(
        )

        # Depuración: Verificar el contenido binario
        print(
            f"Contenido binario del proyecto final (longitud): {len(doc_proyecto_final)}")
        print(
            f"Contenido binario de la carta de presentación (longitud): {len(carta_presentacion_final)}")

        # Asignar el contenido leído al campo binario
        form_proyecto_final.proyecto_final = doc_proyecto_final
        form_proyecto_final.carta_presentacion_final = carta_presentacion_final

        if commit:
            form_proyecto_final.save()

        return form_proyecto_final


class FormActualizarProyectoFinal(forms.ModelForm):
    doc_proyecto_final_form = forms.FileField(required=True)
    carta_presentacion_final_form = forms.FileField(required=True)

    class Meta:
        model = ModelProyectoFinal
        fields = ('doc_proyecto_final_form',
                  'carta_presentacion_final_form',)

    def __init__(self, *args, **kwargs):
        super(FormActualizarProyectoFinal, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['doc_proyecto_final_form'].required = False
            self.fields['carta_presentacion_final_form'].required = False

    def save(self, commit=True):
        form_proyecto_final = super().save(commit=False)

        if self.cleaned_data.get('doc_proyecto_final_form'):
            form_proyecto_final.proyecto_final = self.cleaned_data['doc_proyecto_final_form'].read(
            )

        if self.cleaned_data.get('carta_presentacion_final_form'):
            form_proyecto_final.carta_presentacion_final = self.cleaned_data['carta_presentacion_final_form'].read(
            )

        if commit:
            form_proyecto_final.save()

        return form_proyecto_final

# creacion de cada uno de los formularios del apartado de la linea de tiempo de los objetivos


class FormObjetivoGeneral(forms.ModelForm):
    class Meta:
        model = ModelObjetivoGeneral
        fields = ('descripcion', 'estado')

    def save(self, commit=True):
        objetivo_general = super().save(commit=False)
        objetivo_general.descripcion = self.cleaned_data['descripcion']
        if commit:
            objetivo_general.save()
        return objetivo_general


class FormObjetivosEspecificos(forms.ModelForm):
    class Meta:
        model = ModelObjetivosEspecificos
        fields = ('descripcion', 'estado')

    def save(self, commit=True):
        objetivos_especificos = super().save(commit=False)
        objetivos_especificos.descripcion = self.cleaned_data['descripcion']
        if commit:
            objetivos_especificos.save()
        return objetivos_especificos


class FormActividades(forms.ModelForm):
    class Meta:
        model = ModelActividades
        fields = ('descripcion', 'estado')

    def save(self, commit=True):
        actividades = super().save(commit=False)
        actividades.descripcion = self.cleaned_data['descripcion']
        if commit:
            actividades.save()
        return actividades
