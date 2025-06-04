from django.db import models
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('surgeon', 'Surgeon'),
        ('pharmacist', 'Pharmacist'),
        ('radiologist', 'Radiologist'),
        ('lab_technician', 'Lab Technician'),
        ('therapist', 'Therapist'),
        ('physiotherapist', 'Physiotherapist'),
        ('dietitian', 'Dietitian'),
        ('paramedic', 'Paramedic'),
        ('receptionist', 'Receptionist'),
        ('billing_specialist', 'Billing Specialist'),
        ('medical_assistant', 'Medical Assistant'),
        ('health_information_technician', 'Health Information Technician'),
        ('hospital_manager', 'Hospital Manager'),
        ('human_resources', 'Human Resources'),
        ('janitor', 'Janitor'),
        ('security_guard', 'Security Guard'),
        ('kitchen_staff', 'Kitchen Staff'),
        ('transportation_staff', 'Transportation Staff'),
        ('medical_records_clerk', 'Medical Records Clerk'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='medical_assistant')

class Responsavel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=254, null=True, blank=True)
    sobrenome = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}" if self.nome and self.sobrenome else "Responsável"

class Paciente(models.Model):
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='dependentes', null=True, blank=True)
    nome = models.CharField(max_length=254, null=True, blank=True)
    sobrenome = models.CharField(max_length=254, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}" if self.nome and self.sobrenome else "Paciente"

class Vacina(models.Model):
    vacina = models.CharField(max_length=254, null=True, blank=True)
    fabricante = models.CharField(max_length=254, null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.vacina if self.vacina else "Vacina Não Especificada"

class PacienteVacina(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='vacinas', null=True, blank=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE, related_name='pacientes', null=True, blank=True)
    data_vacinacao = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.paciente} - {self.vacina} ({self.data_vacinacao})" if self.paciente and self.vacina else "Registro de Vacinação Incompleto"
