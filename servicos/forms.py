from django import forms
from django.forms import ModelForm
from .models import Servico

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado', 'protocolo', 'id']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxSelectMultiple':
                # Evita sobrescrever o widget do campo data
                if field_name != 'data':
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'placeholder': field.label or field_name.capitalize()
                    })

        if 'regiao_servico' in self.fields:
            self.fields['regiao_servico'].widget.attrs.update({
                'class': 'form-control'
            })
