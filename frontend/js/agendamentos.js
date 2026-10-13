const API = 'http://127.0.0.1:8000'
const formAgendamento = document.getElementById('form-agendamento')

async function carregarSelects() {
  try {
    // Carregar Clientes para o select
    const resClientes = await fetch(`${API}/clientes`)
    const clientes = await resClientes.json()
    const selectCliente = document.getElementById('cliente_id')
    selectCliente.innerHTML = '<option value="">Selecione um cliente...</option>'
    clientes.forEach(c => {
      selectCliente.innerHTML += `<option value="${c.idcliente}">${c.nome}</option>`
    })

    // Carregar Tatuadores para o select
    const resTatuadores = await fetch(`${API}/tatuadores`)
    const tatuadores = await resTatuadores.json()
    const selectTatuador = document.getElementById('tatuador_id')
    selectTatuador.innerHTML = '<option value="">Selecione um tatuador...</option>'
    tatuadores.forEach(t => {
      selectTatuador.innerHTML += `<option value="${t.idtatuador}">${t.nome}</option>`
    })
  } catch (erro) {
    console.error('Erro ao carregar selects:', erro)
  }
}

async function listarAgendamentos() {
  try {
    const resposta = await fetch(`${API}/agendamentos`)
    const agendamentos = await resposta.json()

    const corpo = document.getElementById('corpo-tabela')
    corpo.innerHTML = ''

    agendamentos.forEach(a => {
      // Se existir um desenho aprovado, mostra a imagem miniatura com link para abrir
      const imagemHtml = a.desenhoaprovado 
        ? `<a href="${API}/uploads/${a.desenhoaprovado}" target="_blank"><img src="${API}/uploads/${a.desenhoaprovado}" width="40" class="rounded shadow-sm"></a>`
        : '<span class="text-muted">Sem imagem</span>'

      corpo.innerHTML += `
        <tr>
          <td>${a.idagendamento}</td>
          <td>${a.cliente}</td>
          <td>${a.tatuador}</td>
          <td>${a.dataagendamento}</td>
          <td>${a.horaagendamento}</td>
          <td>R$ ${a.valortatuagem ? parseFloat(a.valortatuagem).toFixed(2) : '0.00'}</td>
          <td><span class="badge bg-secondary">${a.status || 'pendente'}</span></td>
          <td>${imagemHtml}</td>
          <td>
            <button class="btn btn-sm btn-danger" onclick="deletarAgendamento(${a.idagendamento})">Excluir</button>
          </td>
        </tr>`
    })
  } catch (erro) {
    console.error('Erro ao listar agendamentos:', erro)
  }
}

// Inicializar dados ao carregar a página
carregarSelects().then(() => listarAgendamentos())

// Evento de submissão do formulário (com suporte a ficheiros / FormData)
formAgendamento.addEventListener('submit', async (e) => {
  e.preventDefault()

  const formData = new FormData()
  formData.append('idcliente', document.getElementById('cliente_id').value)
  formData.append('idtatuador', document.getElementById('tatuador_id').value)
  formData.append('dataagendamento', document.getElementById('data').value)
  formData.append('horaagendamento', document.getElementById('hora').value)
  formData.append('descricaotatuagem', document.getElementById('descricao').value)
  formData.append('valortatuagem', document.getElementById('valor').value)
  formData.append('status', document.getElementById('status').value || 'pendente')

  const inputDesenho = document.getElementById('desenho')
  if (inputDesenho.files[0]) {
    formData.append('desenho', inputDesenho.files[0])
  }

  try {
    const resposta = await fetch(`${API}/agendamentos`, {
      method: 'POST',
      body: formData
    })

    if (resposta.ok) {
      formAgendamento.reset()
      listarAgendamentos()
    } else {
      const erroDetalhe = await resposta.json()
      alert('Erro ao criar agendamento: ' + (erroDetalhe.detail || 'Erro desconhecido'))
    }
  } catch (erro) {
    console.error('Erro na requisição:', erro)
    alert('Erro de conexão com o servidor.')
  }
})

async function deletarAgendamento(id) {
  if (!confirm('Tens a certeza que pretendes excluir este agendamento?')) return

  try {
    const resposta = await fetch(`${API}/agendamentos/${id}`, { method: 'DELETE' })
    if (resposta.ok) {
      listarAgendamentos()
    } else {
      alert('Erro ao excluir agendamento.')
    }
  } catch (erro) {
    console.error('Erro ao excluir:', erro)
  }
}