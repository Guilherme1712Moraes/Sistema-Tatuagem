const API = 'http://127.0.0.1:8000'
const formCadastro = document.getElementById('form-cadastro')

formCadastro.addEventListener('submit', async (e) => {
  e.preventDefault()

  const dados = {
    nome: document.getElementById('nome').value,
    email: document.getElementById('email').value,
    senha: document.getElementById('senha').value
  }

  try {
    const resposta = await fetch(`${API}/usuarios/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    })

    const resultado = await resposta.json()

    if (resposta.ok) {
      alert('Conta criada com sucesso! Podes fazer login.')
      window.location.href = 'login.html'
    } else {
      alert('Erro ao cadastrar: ' + (resultado.detail || JSON.stringify(resultado)))
    }
  } catch (erro) {
    console.error('Erro de rede:', erro)
    alert('Erro de conexão com o servidor.')
  }
})