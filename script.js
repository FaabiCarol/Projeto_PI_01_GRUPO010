document.getElementById('agendasindico').addEventListener('submit', function(event) {
    event.preventDefault();

    
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const data = document.getElementById('data').value;
    const arquivo = document.getElementById('arquivo').files[0];

    const demanda = {
        titulo: titulo,
        descricao: descricao,
        data: data,
        arquivo: arquivo ? arquivo.name : 'Nenhum arquivo anexado',
        status: 'pendente' // Inicialmente, todas as demandas são pendentes
    };

    exibirDemanda(demanda);
    this.reset();
});

function exibirDemanda(demanda) {
    const listaDemandas = document.getElementById('listadedemandas');
    const itemDemanda = document.createElement('li');
    itemDemanda.innerHTML = `
        <div>
            <h3>${demanda.titulo}</h3>
            <p><strong>Descrição:</strong> ${demanda.descricao}</p>
            <p><strong>Data:</strong> ${demanda.data}</p>
            <p><strong>Arquivo:</strong> ${demanda.arquivo}</p>
            <p><strong>Status:</strong> <span class="status-${demanda.status}">${demanda.status}</span></p>
        </div>
        <button onclick="alterarStatus(this)">Marcar como Resolvido</button>
    `;
    listaDemandas.appendChild(itemDemanda);
}

function alterarStatus(botao) {
    const itemDemanda = botao.parentElement;
    const statusElement = itemDemanda.querySelector('.status-pendente, .status-resolvido');
    const novoStatus = statusElement.classList.contains('status-pendente') ? 'resolvido' : 'pendente';
    statusElement.textContent = novoStatus;
    statusElement.className = `status-${novoStatus}`;
    botao.textContent = novoStatus === 'resolvido' ? 'Marcar como Pendente' : 'Marcar como Resolvido';
}

document.getElementById('apagarDemandas').addEventListener('click', function() {
    document.getElementById('demandasList').innerHTML = '';
});
