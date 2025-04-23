from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import EstudanteForm
from .models import Estudante
import csv
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from django.views.decorators.http import require_POST




def home(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido_feito')
    else:
        form = EstudanteForm()
    return render(request, 'requisitions/user/home.html', {'form': form})

# Adicione esta view se estiver faltando
def pedido_feito(request):
    return render(request, 'requisitions/user/pedido_feito.html')

@staff_member_required
def relatorio_requisicoes(request):
    estudantes = Estudante.objects.all().order_by('-bolsista_paae', '-created')
    return render(request, 'requisitions/relatorio.html', {'estudantes': estudantes})

@staff_member_required
def exportar_excel(request):
    # Cria um Workbook (arquivo Excel)
    wb = Workbook()
    ws = wb.active
    ws.title = "Estudantes"

    # Cabeçalho (linha 1)
    cabecalho = [
    "Nome", "Matrícula", "Email", "Curso",
    "Caderno", "Data de entrega do caderno",
    "Garrafa", "Data de entrega da garrafa",
    "Camisa", "Tamanho", "Data de entrega da camisa",
    "Sapato", "Data Sapato",
    "Bolsista", "Entregue", "Observações", "Data Pedido"
]

    ws.append(cabecalho)

    # Formatação do cabeçalho (negrito e centralizado)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Preenche os dados
    estudantes = Estudante.objects.all()
    for estudante in estudantes:
        ws.append([
            estudante.nome_estudante,
            estudante.matricula,
            estudante.email,
            estudante.get_curso_display(),
            "Sim" if estudante.deseja_caderno else "Não",
            estudante.data_entrega_caderno.strftime("%d/%m/%Y") if estudante.data_entrega_caderno else "-",
            "Sim" if estudante.deseja_garrafa else "Não",
            estudante.data_entrega_garrafa.strftime("%d/%m/%Y") if estudante.data_entrega_garrafa else "-",
            "Sim" if estudante.deseja_camisa else "Não",
            estudante.tamanho_camisa or "-",
            estudante.data_entrega_camisa.strftime("%d/%m/%Y") if estudante.data_entrega_camisa else "-",
            "Sim" if estudante.deseja_sapato else "Não",
            estudante.data_entrega_sapato.strftime("%d/%m/%Y") if estudante.data_entrega_sapato else "-",
            "Sim" if estudante.bolsista_paae else "Não",
            "Sim" if estudante.pedido_entregue else "Não",
            estudante.observacao or "-",
            estudante.created.strftime("%d/%m/%Y %H:%M")
        ])


    # Ajusta a largura das colunas (opcional)
    for column in ws.columns:
        max_length = 0
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    # Salva o arquivo Excel na resposta HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="estudantes.xlsx"'
    wb.save(response)

    return response


@staff_member_required
def exportar_pdf(request):
    try:
        # Configuração da resposta HTTP
        response = HttpResponse(content_type='application/pdf')
        filename = f"relatorio_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Criando o documento PDF
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']
        subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], spaceAfter=12)

        # Título do PDF
        elements.append(Paragraph("Relatório de Requisições dos Estudantes", title_style))
        elements.append(Spacer(1, 12))

        # Consulta dos estudantes
        estudantes = Estudante.objects.all().order_by('nome_estudante')

        if not estudantes:
            elements.append(Paragraph("Nenhum estudante cadastrado.", normal_style))
        else:
            for estudante in estudantes:
                elements.append(Paragraph(f"Nome: {estudante.nome_estudante}", subtitle_style))
                elements.append(Paragraph(f"Matrícula: {estudante.matricula}", normal_style))
                elements.append(Paragraph(f"Email: {estudante.email}", normal_style))
                elements.append(Paragraph(f"Curso: {estudante.get_curso_display()}", normal_style))
                elements.append(Paragraph(f"Caderno: {'Sim' if estudante.deseja_caderno else 'Não'}", normal_style))
                elements.append(Paragraph(f"Data Entrega Caderno: {estudante.data_entrega_caderno.strftime('%d/%m/%Y') if estudante.data_entrega_caderno else '-'}", normal_style))

                elements.append(Paragraph(f"Garrafa: {'Sim' if estudante.deseja_garrafa else 'Não'}", normal_style))
                elements.append(Paragraph(f"Data Entrega Garrafa: {estudante.data_entrega_garrafa.strftime('%d/%m/%Y') if estudante.data_entrega_garrafa else '-'}", normal_style))

                elements.append(Paragraph(f"Camisa: {'Sim' if estudante.deseja_camisa else 'Não'}", normal_style))
                elements.append(Paragraph(f"Tamanho Camisa: {estudante.tamanho_camisa or '-'}", normal_style))
                elements.append(Paragraph(f"Data Entrega Camisa: {estudante.data_entrega_camisa.strftime('%d/%m/%Y') if estudante.data_entrega_camisa else '-'}", normal_style))

                elements.append(Paragraph(f"Sapato: {'Sim' if estudante.deseja_sapato else 'Não'}", normal_style))
                elements.append(Paragraph(f"Data Entrega Sapato: {estudante.data_entrega_sapato.strftime('%d/%m/%Y') if estudante.data_entrega_sapato else '-'}", normal_style))

                elements.append(Paragraph(f"Bolsista PAAE: {'Sim' if estudante.bolsista_paae else 'Não'}", normal_style))
                elements.append(Paragraph(f"Entregue: {'Sim' if estudante.pedido_entregue else 'Não'}", normal_style))
                elements.append(Paragraph(f"Observação: {estudante.observacao or '-'}", normal_style))
                elements.append(Paragraph(f"Data do Pedido: {estudante.created.strftime('%d/%m/%Y %H:%M')}", normal_style))

                elements.append(Spacer(1, 12))
                elements.append(Paragraph("-" * 100, normal_style))
                elements.append(Spacer(1, 12))

        # Data e hora da exportação
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        elements.append(Paragraph(f"Exportado em: {data_hora}", normal_style))

        # Geração do PDF
        doc.build(elements)

        return response

    except Exception as e:
        return HttpResponse(f"Erro ao gerar PDF: {e}")

@staff_member_required
def relatorio_requisicoes(request):
    estudantes = Estudante.objects.all().order_by('-created')
    return render(request, 'requisitions/relatorio.html', {'estudantes': estudantes})

"""
@staff_member_required
def editar_requisicao(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)
        if form.is_valid():
            form.save()
            return redirect('relatorio')
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'requisitions/editar_requisicao.html', {'form': form})
"""

@staff_member_required
def editar_requisicao(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, instance=estudante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Requisição atualizada com sucesso!')
            return redirect('relatorio')
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'requisitions/editar_requisicao.html', {'form': form, 'estudante': estudante})
"""
@staff_member_required
def excluir_requisicao(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        estudante.delete()
        messages.success(request, 'Requisição excluída com sucesso!')
    return redirect('relatorio')
"""
@require_POST
@staff_member_required
def excluir_requisicao(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    estudante.delete()
    messages.success(request, 'Requisição excluída com sucesso!')
    return redirect('relatorio')
