from django.db import models
from pacientes.models import Paciente
from .choices import ChoicesRegiaoServico
from datetime import datetime
from secrets import token_hex, token_urlsafe
import uuid

# Create your models here.

class RegiaoServico(models.Model):
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2, choices=ChoicesRegiaoServico.choices)
    codigo_postal = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.cidade

class Servico(models.Model):
    
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    
    unidade = models.CharField(max_length=30)
    
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    regiao_servico = models.ManyToManyField(RegiaoServico)  

    data = models.DateField(null=True)
    lote = models.CharField(max_length=50 )
    vacinador = models.CharField( max_length=50 )
    cnes = models.IntegerField(null=True)
    registro_profissional = models.CharField(max_length=50, null=True)
    finalizado = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=54, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.unidade
   
   #sobreescrever o método save()

    def save(self, *args, **kwargs):
        if not self.protocolo:
            data_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
            id_unico = token_hex(4).upper()
            unidade_codigo = self.unidade[:4].upper()
            self.protocolo = f"VAC-{unidade_codigo}-{data_hora}-{id_unico}"

        super(Servico, self).save(*args, **kwargs)




    

