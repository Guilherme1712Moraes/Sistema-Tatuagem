document.getElementById('formCliente').addEventListener('submit', async function (e) {
  e.preventDefault();

  const nome = document.getElementById('nome').value;
  const cpf = document.getElementById('cpf').value;
  const telefone = document.getElementById('telefone').value;

  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch('http://127.0.0.1:8000/clientes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ nome, cpf, telefone })
    });

    if (resposta.ok) {
      alert('Cliente cadastrado com sucesso!');
      document.getElementById('formCliente').reset();
      carregarClientes();
    } else {
      const erro = await resposta.json();
      alert('Erro ao cadastrar cliente: ' + (JSON.stringify(erro.detail) || 'Erro desconhecido'));
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    alert('Não foi possível conectar ao servidor.');
  }
});

async function carregarClientes() {
  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch('http://127.0.0.1:8000/clientes/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (resposta.ok) {
      const clientes = await resposta.json();
      const tbody = document.getElementById('tabelaClientes');

      if (!tbody) return;

      tbody.innerHTML = '';

      clientes.forEach(cliente => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${cliente.nome}</td>
          <td>${cliente.telefone || 'Não informado'}</td>
          <td>
            <button class="btn btn-danger btn-sm" onclick="deletarCliente(${cliente.idcliente})">Excluir</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (error) {
    console.error('Erro ao carregar clientes:', error);
  }
}

async function deletarCliente(id) {
  if (!confirm('Tens a certeza de que pretendes excluir este cliente?')) {
    return;
  }

  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch(`http://127.0.0.1:8000/clientes/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const dados = await resposta.json().catch(() => ({}));

    if (resposta.ok && !dados.erro) {
      alert('Cliente excluído com sucesso!');
      carregarClientes();
    } else {
      alert('Erro ao excluir cliente: ' + (dados.detail || dados.erro || 'Erro desconhecido'));
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    alert('Não foi possível conectar ao servidor.');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  carregarClientes();
});