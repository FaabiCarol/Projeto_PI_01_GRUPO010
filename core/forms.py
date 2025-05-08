from django import forms
from django.contrib.auth.models import User
from .models import Morador, Solicitacao

# Formulário para Morador (mantido como fornecido)
class MoradorForm(forms.ModelForm):
    usuario = forms.CharField(required=True, label="Nome de Usuário")
    nome = forms.CharField(required=True, label="Nome Completo")
    email = forms.EmailField(required=True, label="Email")
    telefone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: (11) 99999-9999'}),
        label="Telefone"
    )
    senha = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'name': 'senha'}),
        label="Senha"
    )
    senha_confirmacao = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'name': 'senha_confirmacao'}),
        label="Confirme a Senha"
    )

    class Meta:
        model = Morador
        fields = ['nome', 'email', 'telefone', 'foto_perfil']
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_confirmacao = cleaned_data.get("senha_confirmacao")

        if senha and senha_confirmacao and senha != senha_confirmacao:
            self.add_error('senha_confirmacao', 'As senhas não coincidem.')

        return cleaned_data

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if User.objects.filter(username=usuario).exists():
            raise forms.ValidationError("Já existe um usuário com este nome de usuário.")
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email

    def save(self, commit=True):
        print("Iniciando save do MoradorForm")
        usuario_nome = self.cleaned_data['usuario']
        email = self.cleaned_data['email']
        senha = self.cleaned_data['senha']
        print(f"Dados do formulário: usuario={usuario_nome}, email={email}")

        try:
            usuario = User.objects.create_user(
                username=usuario_nome,
                email=email,
                password=senha
            )
            print(f"Usuário criado: id={usuario.id}, username={usuario.username}")
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            raise

        morador = super().save(commit=False)
        print("Objeto Morador criado (não salvo):", morador.__dict__)
        morador.usuario = usuario
        print("Após associar usuário:", morador.__dict__, "usuario_id=", morador.usuario.id if morador.usuario else None)

        if commit:
            try:
                morador.save()
                print("Morador salvo com sucesso: id=", morador.id)
            except Exception as e:
                print(f"Erro ao salvar Morador: {str(e)}")
                raise

        return morador
# Formulário para Solicitação
class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['origem', 'titulo', 'descricao', 'data', 'status', 'prioridade']
        widgets = {
            'origem': forms.TextInput(attrs={'placeholder': 'Ex: Apartamento 101'}),
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Vazamento na pia'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descreva o problema...', 'rows': 4}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'arquivo': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
            'status': forms.Select(choices=[
                ('pendente', 'Pendente'),
                ('em_andamento', 'Em Andamento'),
                ('resolvido', 'Resolvido')
            ]),
            'prioridade': forms.Select(choices=[
                ('verde', 'Não Urgente'),
                ('amarelo', 'Urgente, mas não importante'),
                ('vermelho', 'Urgente e importante')
            ]),
        }

