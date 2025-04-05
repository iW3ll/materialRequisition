from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import EstudanteForm
from .models import Estudante
import csv
from django.http import HttpResponse


def home(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido_feito')
    else:
        form = EstudanteForm()

    return render(request, 'requisitions/user/home.html', {'form': form})

def pedido_feito(request):
    return render(request, 'requisitions/user/pedido_feito.html')


@staff_member_required
def relatorio_requisicoes(request):
    estudantes = Estudante.objects.all().order_by('-created')
    # Escolha uma das opções:
    return render(request, 'requisitions/relatorio.html', {'estudantes': estudantes}) 
   

@staff_member_required
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="requisicoes_materiais.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Nome', 'Matrícula', 'Email', 'Curso', 
        'Caderno', 'Garrafa', 'Camisa', 
        'Tamanho Camisa', 'Bolsista PAAE', 'Data Registro'
    ])
    
    for estudante in Estudante.objects.all():
        writer.writerow([
            estudante.nome_estudante,
            estudante.matricula,
            estudante.email,
            estudante.get_curso_display(),
            'Sim' if estudante.deseja_caderno else 'Não',
            'Sim' if estudante.deseja_garrafa else 'Não',
            'Sim' if estudante.deseja_camisa else 'Não',
            estudante.get_tamanho_camisa_display() if estudante.tamanho_camisa else '-',
            'Sim' if estudante.bolsista_paae else 'Não',
            estudante.created.strftime('%d/%m/%Y %H:%M')
        ])
    
    return response