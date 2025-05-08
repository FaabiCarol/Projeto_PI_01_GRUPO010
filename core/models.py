from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

class Condominio(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nome

class Morador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Solicitacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    origem = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateField()
    arquivo = models.FileField(upload_to='arquivo/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
    ], default='pendente')
    prioridade = models.CharField(max_length=20, choices=[
        ('verde', 'Não Urgente'),
        ('amarelo', 'Urgente, mas não importante'),
        ('vermelho', 'Urgente e importante'),
    ], default='verde')

    def __str__(self):
        return self.titulo



