from django.urls import path
from .views import home, pedido_feito, relatorio_requisicoes,editar_requisicao, excluir_requisicao
from .views import exportar_excel, exportar_pdf
#exportar_csv,

urlpatterns = [
    path('', home, name='home'),
    path('pedido-feito/', pedido_feito, name='pedido_feito'),
    path('relatorio/', relatorio_requisicoes, name='relatorio'),
    path('relatorio/editar/<int:pk>/', editar_requisicao, name='editar_requisicao'),
    path('excluir/<int:pk>/', excluir_requisicao, name='excluir_requisicao'),
    #path('exportar-csv/', exportar_csv, name='exportar_csv'),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),
    
]