from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paciente, Vacina, PacienteVacina, Responsavel
from django.core import serializers
import json
import re
from datetime import datetime
from django.views import View
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
import json
import re


class ResponsaveisViewAPI(View):
    def get(self, request):
        try:
            responsaveis = Responsavel.objects.get()
            return JsonResponse({'responsaveis': responsaveis})
        except Responsavel.DoesNotExist:
            responsaveis = None
    
def post(self, request):
    data = request.POST 

    responsaveis = Responsavel.objects.all()
    lista_responsaveis = []

    for r in responsaveis:
        lista_responsaveis.append({
            "nome": r.nome,
            "sobrenome": r.sobrenome,
            "email": r.email,
            "cpf": r.cpf,
            "rg": r.rg,
            "telefone": r.telefone,
            "data_nascimento": r.data_nascimento.strftime('%Y-%m-%d') if r.data_nascimento else None,
            "parentesco": r.parentesco,
            "endereco": r.endereco,
            "numero": r.numero,
            "complemento": r.complemento,
            "bairro": r.bairro,
            "cidade": r.cidade,
            "estado": r.estado,
            "cep": r.cep,
        })

    return JsonResponse({"responsaveis": lista_responsaveis})

class PacienteView(View):
    def get(self, request):
        return render(request, 'pacientes.html')

class PacienteViewAPI(View):  
    def get(self, request):
        pacientes = list(Paciente.objects.values())
        return JsonResponse({'pacientes': pacientes})
    
    def post(self, request):
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        vacinas_json = request.POST.get('vacinas')
        data_vacinacao = request.POST.get('data_vacinacao')

        if Paciente.objects.filter(cpf=cpf).exists():
            return JsonResponse({'status': 400, 'message': 'Paciente com este CPF já existe.'})

        try:
            vacinas = json.loads(vacinas_json)
        except (TypeError, json.JSONDecodeError):
            return JsonResponse({'status': 400, 'message': 'Erro ao processar vacinas.'})
        
        try:
            data_nascimento_str = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return JsonResponse({'status': 400, 'message': 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'})

        paciente = Paciente.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            data_nascimento=data_nascimento_str
        )

        for v in vacinas:
            vacina = Vacina.objects.create(
                vacina=v['vacina'],
                fabricante=v['fabricante'],
                codigo=v['codigo']
            )

            data_vacinacao_str = v.get('data_vacinacao', data_vacinacao)
            try:
                data_vacinacao = datetime.strptime(data_vacinacao_str, "%Y-%m-%d").date() if data_vacinacao_str else None
            except ValueError:
                return JsonResponse({'status': 400, 'message': f'Data de vacinação inválida para vacina {v.get("vacina")}.'})
                                    
            PacienteVacina.objects.create(
                paciente=paciente,
                vacina=vacina,
                data_vacinacao=data_vacinacao
            )

        return JsonResponse({'status': 200, 'message': 'Paciente e vacinas cadastrados com sucesso!'})
    
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
            
            paciente.cpf = dataBody['cpf']
            try:
                data_nascimento = datetime.strptime(dataBody['data_nascimento'], "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({'status': 400, 'error': 'Formato de data inválido. Use YYYY-MM-DD.'})
            
            paciente.data_nascimento = data_nascimento

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