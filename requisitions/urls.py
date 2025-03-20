from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pedido-feito/', views.pedido_feito, name='pedido_feito'),
]