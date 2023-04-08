from django.db import models
from pacientes.models import Paciente
from .choices import ChoicesRegiaoServico
from datetime import datetime
from secrets import token_hex

# Create your models here.

class RegiaoServico(models.Model):
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2, choices=ChoicesRegiaoServico.choices)
    codigo_postal = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.cidade

class Servico(models.Model):
    unidade = models.CharField(max_length=30)
    
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    regiao_servico = models.ManyToManyField(RegiaoServico)  

    data = models.DateField(null=True)
    lote = models.CharField(max_length=50 )
    vacinador = models.CharField( max_length=50 )
    cnes = models.IntegerField(null=True)
    registro_profissional = models.CharField(max_length=50, null=True)
    finalizado = models.BooleanField(default=True)
    protocolo = models.CharField(max_length=54, null=True, blank=True)
    def __str__(self) -> str:
        return self.unidade
   
   #sobreescrever o método save()

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime("%d/%m/%Y - %H:%M:%S - ") + token_hex(16) #mantem data e hora com o token
        super(Servico, self).save(*args, **kwargs) #executa método save





    

