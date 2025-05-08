document.getElementById('agendasindico').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio normal do formulário
    
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const data = document.getElementById('data').value;
    const arquivo = document.getElementById('arquivo').files[0];
    
    // Cria um FormData para enviar o arquivo junto com os outros dados
    const formData = new FormData();
    formData.append('titulo', titulo);
    formData.append('descricao', descricao);
    formData.append('data', data);
    formData.append('arquivo', arquivo ? arquivo : null);
    
    // Envia os dados via AJAX
    fetch('/salvar_solicitacao/', { // Supondo que a URL para salvar a solicitação seja /salvar_solicitacao/
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redireciona para a página de listagem de solicitações
            window.location.href = '/listar_solicitacoes/'; // Altere a URL conforme necessário
        } else {
            alert('Ocorreu um erro ao salvar a demanda. Tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro inesperado.');
    });
});
