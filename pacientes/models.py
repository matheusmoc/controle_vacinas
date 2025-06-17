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
    PARENTESCO_CHOICES = [
        ('pai', 'Pai'),
        ('mae', 'Mãe'),
        ('avo', 'Avô/Avó'),
        ('tio', 'Tio(a)'),
        ('outro', 'Outro'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField("Nome", max_length=254, null=True, blank=True)
    sobrenome = models.CharField("Sobrenome", max_length=254, null=True, blank=True)
    email = models.EmailField("Email", max_length=254, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, null=True, blank=True)
    rg = models.CharField("RG", max_length=20, null=True, blank=True)
    telefone = models.CharField("Telefone", max_length=20, null=True, blank=True)
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    parentesco = models.CharField("Parentesco com a criança", max_length=10, choices=PARENTESCO_CHOICES, null=True, blank=True)

    endereco = models.CharField("Endereço", max_length=255, null=True, blank=True)
    numero = models.CharField("Número", max_length=10, null=True, blank=True)
    complemento = models.CharField("Complemento", max_length=50, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=100, null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=100, null=True, blank=True)
    estado = models.CharField("Estado", max_length=2, null=True, blank=True)
    cep = models.CharField("CEP", max_length=9, null=True, blank=True)

    observacoes = models.TextField("Observações", null=True, blank=True)

    def __str__(self) -> str:
        if self.nome and self.sobrenome:
            return f"{self.nome} {self.sobrenome}"
        elif self.nome:
            return self.nome
        else:
            return "Responsável"

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

class Paciente(models.Model):
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='dependentes', null=True, blank=True)
    nome = models.CharField(max_length=254, null=True, blank=True)
    sobrenome = models.CharField(max_length=254, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='dependentes', null=True, blank=True)

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
