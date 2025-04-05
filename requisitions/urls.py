from django.urls import path
from .views import home, pedido_feito, relatorio_requisicoes, exportar_csv

urlpatterns = [
    path('', home, name='home'),
    path('pedido-feito/', pedido_feito, name='pedido_feito'),
    path('relatorio/', relatorio_requisicoes, name='relatorio'),
    path('exportar-csv/', exportar_csv, name='exportar_csv'),
]