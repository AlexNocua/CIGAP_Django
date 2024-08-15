from .models import ModelLoginUser


class FormLogin(forms.ModelForm):
    model = ModelLoginUser
    fields = '__all__'
