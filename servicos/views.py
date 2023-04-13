from django.shortcuts import render, get_object_or_404
from .forms import FormServico
from django.http import HttpResponse, FileResponse
from .models import Servico
from pacientes.models import Vacina
from fpdf import FPDF
from io import BytesIO

# Create your views here.


def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'novo_servico.html', {'form_servico': form})
    elif request.method == "POST":
        form = FormServico(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('Salvo com sucesso')
        else:
            return render(request, 'novo_servico.html',{'form_servico' : form})

def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, 'listar_servico.html', {'servicos': servicos})

def servico(request, identificador):       #coluna       #filtro passado por paramento
    servico = get_object_or_404(Servico, identificador=identificador )
    # return HttpResponse(identificador)
    return render(request, 'servico.html',{'servico' : servico})

def gerar_carteira_vacinacao(request, identificador):
    servico = get_object_or_404(Servico, identificador = identificador)
    
    pdf = FPDF() #INSTANCIA PARA GERAR AS CARTEIRINHAS
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.set_fill_color(240, 240, 240)

    pdf.cell(40, 10, 'CARTEIRINHA DE VACINAÇÃO', 0, 1)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Paciente:', 0, 0)
    pdf.cell(0, 10, f'{servico.paciente.nome} {servico.paciente.sobrenome}', 0, 1)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Região:', 0, 0)
    
    regiao_servico = servico.regiao_servico.all()
    for i, regiao in enumerate(regiao_servico) :
        pdf.cell(0, 10, f'{regiao.cidade} - {regiao.estado}', 0, 1)
        if not i == len(regiao_servico) - 1:
            pdf.cell(0, 10, '', 0, 1)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Data de nascimento:', 0, 0)
    pdf.cell(0, 10, f'  ___/___/____', 0, 1)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Vacina:', 0, 0)
    pdf.cell(0, 10, '--', 0, 1)


    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Data da vacinação:', 0, 0)
    pdf.cell(0, 10, str(servico.data), 0, 1)


    
    # cria uma tabela de 3x1 células
    for i in range(1):
        for j in range(4):
            pdf.cell(40, 10, f"Célula ({i}, {j})", border=1)
        pdf.ln()  # quebra de linha
            # cria uma tabela de 3x1 células
    for i in range(1):
        for j in range(4):
            pdf.cell(40, 10, f"Célula ({i}, {j})", border=1)
        pdf.ln()  # quebra de linha
            # cria uma tabela de 3x1 células
    for i in range(1):
        for j in range(4):
            pdf.cell(40, 10, f"Célula ({i}, {j})", border=1)
        pdf.ln()  # quebra de linha
            # cria uma tabela de 3x1 células
    for i in range(1):
        for j in range(4):
            pdf.cell(40, 10, f"Célula ({i}, {j})", border=1)
        pdf.ln()  # quebra de linha
    

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 30, 'Protocolo:', 0, 0)
    pdf.cell(0, 30, str(servico.protocolo), 0, 1)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_byte = BytesIO(pdf_content)
    return FileResponse(pdf_byte, as_attachment=True, filename=f"carteirinha-{servico.protocolo}.pdf")