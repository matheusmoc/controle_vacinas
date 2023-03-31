from django.shortcuts import render
from django.http import HttpResponse
from .models import Paciente, Vacina
import re


def pacientes(request):
    if request.method == 'GET':
        return render(request, 'pacientes.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')

        vacinas = request.POST.getlist('vacina')
        fabricantes = request.POST.getlist('fabricante')
        codigos = request.POST.getlist('codigo')

        paciente = Paciente.objects.filter(cpf=cpf)
        if paciente.exists():
            return render(request, 'pacientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'vacinas': zip(vacinas, fabricantes, codigos)})
            # return HttpResponse('Paciente já cadastrado')

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
             return render(request, 'pacientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'vacinas': zip(vacinas, fabricantes, codigos)})
        # Cria um objeto Paciente e salva no banco de dados
        pacientes = Paciente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf
        )

        pacientes.save()

        # Cria um objeto Vacina para cada item das listas de vacinas, fabricantes e códigos,
        # utilizando a variável pacientes como parâmetro
        for vacinas, fabricantes, codigos in zip(vacinas, fabricantes, codigos):
            vac = Vacina(vacina=vacinas, fabricante=fabricantes,
                         codigo=codigos, paciente=pacientes)
            vac.save()

        return HttpResponse('teste')
