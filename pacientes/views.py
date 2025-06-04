from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paciente, Vacina, PacienteVacina, Responsavel
from django.core import serializers
import json
import re
from django.views import View
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
import json
import re


class PacienteView(View):
    def get(self, request):
        pacientes_list = Paciente.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes_list})

    def post(self, request):
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')

        vacinas = request.POST.getlist('vacina')
        fabricantes = request.POST.getlist('fabricante')
        codigos = request.POST.getlist('codigo')

        if Paciente.objects.filter(cpf=cpf).exists():
            return render(request, 'pacientes.html', {
                'nome': nome,
                'sobrenome': sobrenome,
                'email': email,
                'vacinas': zip(vacinas, fabricantes, codigos)
            })

        if not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            return render(request, 'pacientes.html', {
                'nome': nome,
                'sobrenome': sobrenome,
                'cpf': cpf,
                'vacinas': zip(vacinas, fabricantes, codigos)
            })
        
        responsavel_id = request.POST.get('responsavel_id') 
        responsavel = Responsavel.objects.get(id=responsavel_id)

        paciente = Paciente(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            responsavel=responsavel 
        )
        paciente.save()

        for vacina_nome, fabricante, codigo in zip(vacinas, fabricantes, codigos):
            vacina = Vacina.objects.create(
                vacina=vacina_nome,
                fabricante=fabricante,
                codigo=codigo
            )
            PacienteVacina.objects.create(
                paciente=paciente,
                vacina=vacina,
                data_vacinacao=request.POST.get('data_vacinacao') 
            )

        return HttpResponse('Paciente e vacinas cadastrados com sucesso!')

    def att_paciente(request):
        id_paciente = request.POST.get('id_paciente')
        paciente = get_object_or_404(Paciente, id=id_paciente)
        vacinas = Vacina.objects.filter(pacientes__paciente=paciente)

        # Serializando paciente e vacinas
        pacientes_json = json.loads(serializers.serialize('json', [paciente]))[0]['fields']
        vacinas_json = json.loads(serializers.serialize('json', vacinas))

        vacinas_json = [{'fields': vacina['fields'], 'id': vacina['pk']} for vacina in vacinas_json]

        data = {
            'paciente': pacientes_json,
            'vacinas': vacinas_json
        }
        return JsonResponse(data)

    def update_paciente(request, id):
        if request.method == 'POST':
            dataBody = json.loads(request.body)
            paciente = get_object_or_404(Paciente, id=id)
            paciente.nome = dataBody['nome']
            paciente.sobrenome = dataBody['sobrenome']
            paciente.email = dataBody['email']
            paciente.cpf = dataBody['cpf']

            try:
                paciente.save()
                data = serializers.serialize('json', [paciente])
                return JsonResponse({'status': 200, 'data': data})
            except Exception as e:
                return JsonResponse({'status': 500, 'error': str(e)})
            
class VacinaView(View):
    @csrf_exempt
    def update_vacina(request, id):
        if request.method == 'POST':
            nome_vacina = request.POST.get('vacina')
            codigo = request.POST.get('codigo')
            fabricante = request.POST.get('fabricante')

            if not nome_vacina or not codigo or not fabricante:
                return HttpResponse('O campo vacina é obrigatório.')

            vacina = get_object_or_404(Vacina, id=id)
            if Vacina.objects.filter(codigo=codigo).exclude(id=id).exists():
                return HttpResponse('A vacina já foi aplicada neste paciente.')

            vacina.vacina = nome_vacina
            vacina.codigo = codigo
            vacina.fabricante = fabricante
            vacina.save()
            
            return HttpResponse("Dados alterados com sucesso!")

    def excluir_vacina(request, id):
        vacina = get_object_or_404(Vacina, id=id)
        vacina.delete()
        return redirect('pacientes') 

class RelatorioStatusVacinalView(View):
    def get_report(request):
        return render(request, 'vaccination_report.html')
    

class HistoricoVacinalView(View):
    def get_history(request):
        return render(request, 'vaccination_history.html')