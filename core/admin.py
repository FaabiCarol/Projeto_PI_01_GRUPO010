from django.contrib import admin
from .models import Morador, Solicitacao
from core.models import Condominio

admin.site.register(Morador)
admin.site.register(Solicitacao)
Condominio.objects.all()
