const API = 'http://127.0.0.1:8000'
const formTatuador = document.getElementById('form-tatuador')
const botaoSubmit = document.getElementById('btn-submit-tatuador')

async function carregarSelects() {
  // Carrega Senioridades
  const resSen = await fetch(`${API}/senioridade`)
  const senioridades = await resSen.json()
  const selectSen = document.getElementById('idsenioridade')
  selectSen.innerHTML = '<option value="">Selecione a senioridade...</option>'
  senioridades.forEach(s => {
    selectSen.innerHTML += `<option value="${s.idsenioridade}">${s.nome}</option>`
  })

  // Carrega Estilos em Checkboxes
  const resEst = await fetch(`${API}/estilos`)
  const estilos = await resEst.json()
  const divEstilos = document.getElementById('lista-estilos-checkbox')
  divEstilos.innerHTML = ''
  estilos.forEach(e => {
    divEstilos.innerHTML += `
      <div class="form-check">
        <input class="form-check-input estilo-checkbox" type="checkbox" value="${e.idestilo}" id="estilo_${e.idestilo}">
        <label class="form-check-label" for="estilo_${e.idestilo}">
          ${e.descricao}
        </label>
      </div>`
  })
}

async function listarTatuadores() {
  const resposta = await fetch(`${API}/tatuadores`)
  const tatuadores = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  tatuadores.forEach(t => {
    const estilosNomes = t.estilos.map(e => e.descricao).join(', ') || 'Nenhum'
    corpo.innerHTML += `
      <tr>
        <td>${t.idtatuador}</td>
        <td>${t.nome}</td>
        <td>${t.senioridade_nome || t.idsenioridade}</td>
        <td>${estilosNomes}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherEdicao(${JSON.stringify(t)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarTatuador(${t.idtatuador})">Excluir</button>
        </td>
      </tr>`
  })
}

// Inicializar dados da página
carregarSelects().then(() => listarTatuadores())

formTatuador.addEventListener('submit', async (e) => {
  e.preventDefault()

  const nome = document.getElementById('nome').value
  const idsenioridade = parseInt(document.getElementById('idsenioridade').value)
  
  // Recolher IDs de todos os checkboxes selecionados
  const estilosSelecionados = Array.from(document.querySelectorAll('.estilo-checkbox:checked'))
    .map(cb => parseInt(cb.value))

  const tatuador = { nome, idsenioridade, estilos: estilosSelecionados }
  const idTatuador = formTatuador.dataset.idTatuador

  if (idTatuador) {
    await fetch(`${API}/tatuadores/${idTatuador}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  } else {
    await fetch(`${API}/tatuadores`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  }

  formTatuador.reset()
  delete formTatuador.dataset.idTatuador
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
  
  // Desmarcar checkboxes
  document.querySelectorAll('.estilo-checkbox').forEach(cb => cb.checked = false)

  listarTatuadores()
})

function preencherEdicao(tatuador) {
  document.getElementById('nome').value = tatuador.nome
  document.getElementById('idsenioridade').value = tatuador.idsenioridade
  formTatuador.dataset.idTatuador = tatuador.idtatuador

  // Marcar os checkboxes correspondentes aos estilos atuais do tatuador
  const idsEstilosTatuador = tatuador.estilos.map(e => e.idestilo)
  document.querySelectorAll('.estilo-checkbox').forEach(cb => {
    cb.checked = idsEstilosTatuador.includes(parseInt(cb.value))
  })

  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

async function deletarTatuador(id) {
  if (!confirm('Tem certeza que deseja excluir este tatuador?')) return
  await fetch(`${API}/tatuadores/${id}`, { method: 'DELETE' })
  listarTatuadores()
}