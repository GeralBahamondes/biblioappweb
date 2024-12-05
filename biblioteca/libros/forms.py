from django import forms
from .models import Libro, GENEROS_CHOICES

class LibroForm(forms.ModelForm):
    genero = forms.ChoiceField(choices=GENEROS_CHOICES + [('', 'Seleccione un género')], required=False)
    genero_personalizado = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'genero', 'genero_personalizado', 'cantidad', 'disponible', 'imagen', 'restriccion_edad']

    def clean(self):
        cleaned_data = super().clean()
        genero = cleaned_data.get('genero')
        genero_personalizado = cleaned_data.get('genero_personalizado')

        if genero == 'Otro' and not genero_personalizado:
            raise forms.ValidationError("Por favor, especifique un género personalizado.")

        if genero == 'Otro':
            cleaned_data['genero'] = genero_personalizado

        return cleaned_data