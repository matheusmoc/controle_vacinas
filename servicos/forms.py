from django.forms import ModelForm
from .models import Servico, RegiaoServico

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado', 'protocolo'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label or field_name.capitalize()
            })

        if 'regiao_servico' in self.fields:
            choices = []
            for value, label in self.fields['regiao_servico'].choices:
                if label:  
                    # Evita rótulos vazios (como a opção inicial)
                    # Aqui 'label' é geralmente o __str__() do objeto relacionado
                    choices.append((value, str(label)))
            self.fields['regiao_servico'].choices = choices