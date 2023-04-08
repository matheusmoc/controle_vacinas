from django.forms import ModelForm
from .models import Servico, RegiaoServico

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado', 'protocolo'] #excessão de campos
        
    #acesso ao atributo do ModelForm sobrepondo metódo
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in  self.fields: ##Todas as keys do dicionário
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
            self.fields[field].widget.attrs.update({'placeholder' : field})

        choices = []
        for i, j in self.fields['regiao_servico'].choices:
            label = f"{i} - {j}" # Combine the city name and state abbreviation
            choices.append((i.value, label))
                
        self.fields['regiao_servico'].choices = choices