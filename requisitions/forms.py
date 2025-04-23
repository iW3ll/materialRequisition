from django import forms
from django.forms.widgets import DateInput
from .models import Estudante

class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'nome_estudante', 'matricula', 'email', 'curso',
            'bolsista_paae', 'deseja_caderno', 'deseja_garrafa',
            'deseja_camisa', 'tamanho_camisa', 'pedido_entregue', 'observacao',
            'data_entrega_camisa', 'data_entrega_garrafa', 'data_entrega_caderno' #'data_entrega_sapato', 
        ]
        widgets = {
            'tamanho_camisa': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite observações sobre o pedido...'
            }),
            'pedido_entregue': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_entrega_caderno': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrega_camisa': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrega_garrafa': DateInput(attrs={'type': 'date', 'class': 'form-control'})
            #'data_entrega_sapato': DateInput(attrs={'type': 'date', 'class': 'form-control'})
            
            
        }
