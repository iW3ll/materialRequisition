from django.shortcuts import render, redirect
from .forms import EstudanteForm

def home(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
            return redirect('pedido_feito')  # Redireciona para a página de confirmação
    else:
        form = EstudanteForm()  # Exibe um formulário vazio para requisições GET

    return render(request, 'requisitions/user/home.html', {'form': form})

def pedido_feito(request):
    return render(request, 'requisitions/user/pedido_feito.html')