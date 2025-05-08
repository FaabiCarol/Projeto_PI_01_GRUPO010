from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Solicitacao, Condominio, Morador
from .forms import MoradorForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse



def home(request):
    return render(request, 'home.html')


@login_required
def index(request):
    if request.method == 'POST':
        # Obter dados do formulário
        origem = request.POST.get('origem')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        status = request.POST.get('status')
        prioridade = request.POST.get('prioridade')
        arquivo = request.FILES.get('arquivo')

        # Validação básica
        if not all([origem, titulo, descricao, data]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'index.html')

        # Criar instância de Solicitacao
        solicitacao = Solicitacao(
            usuario=request.user,  # Define o usuário logado
            origem=origem,
            titulo=titulo,
            descricao=descricao,
            data=data,
            status=status or 'pendente',  # Valor padrão se não fornecido
            prioridade=prioridade or 'verde',  # Valor padrão se não fornecido
            arquivo=arquivo
        )
        solicitacao.save()

        messages.success(request, 'Solicitação registrada com sucesso!')
        return redirect('listar_solicitacoes') 

    return render(request, 'index.html')

@login_required
def listar_solicitacoes(request):
    print(f"Usuário logado: {request.user.id}, {request.user.username}")  # Depuração
    solicitacoes = Solicitacao.objects.filter(usuario=request.user)
    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')
    prioridade = request.GET.get('prioridade', '')
    solicitacoes = Solicitacao.objects.filter(usuario=request.user)

    if busca:
        solicitacoes = solicitacoes.filter(titulo__icontains=busca) | solicitacoes.filter(descricao__icontains=busca)
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    if prioridade:
        solicitacoes = solicitacoes.filter(prioridade=prioridade)

    solicitacoes = solicitacoes.order_by('-id')
    paginator = Paginator(solicitacoes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'solicitacoes/listar_solicitacoes.html', {
        'page_obj': page_obj,
        'busca': busca,
        'status': status,
        'prioridade': prioridade,
    })


def apagar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)
    solicitacao.delete()
    return redirect('listar_solicitacoes')


@csrf_protect
@login_required
def alterar_prioridade(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if request.method == 'POST':
        nova_prioridade = request.POST.get('prioridade')
        if nova_prioridade in ['verde', 'amarelo', 'vermelho']:
            solicitacao.prioridade = nova_prioridade
            solicitacao.save()
            
            # Verificar se é uma solicitação AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                # Redirecionar para a página de solicitações com os parâmetros de consulta
                query_params = request.GET.urlencode()
                return redirect(f'{reverse("solicitacoes")}?{query_params}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Prioridade inválida'}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    return redirect('solicitacoes')


@csrf_protect
@login_required
def alterar_status(request, solicitacao_id):
    solicitacao = get_object_or_404(Solicitacao, id=solicitacao_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in ['pendente', 'em_andamento', 'resolvido']:
            solicitacao.status = novo_status
            solicitacao.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                query_params = request.GET.urlencode()
                return redirect(f'{reverse("solicitacoes")}?{query_params}')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Status inválido'}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    return redirect('solicitacoes')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Confirme se 'index' é a URL correta
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import MoradorForm

def cadastro_view(request):
    print("Executando cadastro_view")
    if request.method == 'POST':
        print("Dados enviados:", request.POST)
        form = MoradorForm(request.POST, request.FILES)
        if form.is_valid():
            print("Formulário válido, dados limpos:", form.cleaned_data)
            try:
                morador = form.save()
                print(f"Morador salvo: id={morador.id}, nome={morador.nome}")
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect('index')
            except Exception as e:
                messages.error(request, f"Erro ao salvar o cadastro: {str(e)}")
                print("Erro ao salvar:", str(e))
        else:
            messages.error(request, "Erro no preenchimento do formulário. Verifique os campos.")
            print("Formulário inválido:", form.errors)
    else:
        form = MoradorForm()
    return render(request, 'cadastro.html', {'form': form})


@login_required
def salvar_solicitacao(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        arquivo = request.FILES.get('arquivo')

        # Validação básica
        if not all([titulo, descricao, data]):
            return JsonResponse({'success': False, 'error': 'Preencha todos os campos obrigatórios'}, status=400)

        # Criação do objeto Solicitação
        solicitacao = Solicitacao(
            usuario=request.user,  # Define o usuário logado
            titulo=titulo,
            descricao=descricao,
            data=data,
            arquivo=arquivo,
            status='pendente'
        )
        solicitacao.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)