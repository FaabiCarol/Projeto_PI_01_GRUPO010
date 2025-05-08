from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('solicitacoes/', views.listar_solicitacoes, name='listar_solicitacoes'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('salvar_solicitacao/', views.salvar_solicitacao, name='salvar_solicitacao'),
    path('apagar/<int:id>/', views.apagar_solicitacao, name='apagar_solicitacao'),
    path('alterar_prioridade/<int:id>/', views.alterar_prioridade, name='alterar_prioridade'),
    path('alterar_status/<int:id>/', views.alterar_status, name='alterar_status'),  # URL para alterar status
    path('listar_solicitacoes/', views.listar_solicitacoes, name='listar_solicitacoes'),
    path('solicitacoes/', views.listar_solicitacoes, name='solicitacoes'),
    path('solicitacoes/<int:solicitacao_id>/alterar_prioridade/', views.alterar_prioridade, name='alterar_prioridade'),
    path('solicitacoes/<int:solicitacao_id>/alterar_status/', views.alterar_status, name='alterar_status'),
    path('solicitacoes/<int:solicitacao_id>/apagar/', views.apagar_solicitacao, name='apagar_solicitacao'),
]

