from django import forms
from .models import Estudante

class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'nome_estudante', 'matricula', 'email', 'curso',
            'bolsista_paae', 'deseja_caderno', 'deseja_garrafa',
            'deseja_camisa', 'tamanho_camisa'
        ]
        widgets = {
            'tamanho_camisa': forms.Select(attrs={'class': 'form-control'}),
        }