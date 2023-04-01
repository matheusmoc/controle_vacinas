from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Paciente, Vacina
import re
from django.core import serializers
import json


def pacientes(request):
    if request.method == 'GET':
        pacientes_list = Paciente.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes_list})
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




def att_paciente(request):
    id_paciente = request.POST.get('id_paciente')
    paciente = Paciente.objects.filter(id=id_paciente)
    paciente_json = json.loads(serializers.serialize('json', paciente))[0]['fields']
    # print(cliente_json)
    return JsonResponse(paciente_json)