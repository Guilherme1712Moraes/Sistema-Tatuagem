document.getElementById('formSenioridade').addEventListener('submit', async function (e) {
  e.preventDefault();

  const nivel = document.getElementById('nivel').value;
  const descricao = document.getElementById('descricao').value;
  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch('http://127.0.0.1:8000/senioridade/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ nivel, descricao })
    });

    if (resposta.ok) {
      alert('Senioridade cadastrada com sucesso!');
      document.getElementById('formSenioridade').reset();
      carregarSenioridades();
    } else {
      const erro = await resposta.json();
      alert('Erro ao cadastrar: ' + JSON.stringify(erro.detail || erro));
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    alert('Não foi possível conectar ao servidor.');
  }
});

async function carregarSenioridades() {
  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch('http://127.0.0.1:8000/senioridade/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (resposta.ok) {
      const dados = await resposta.json();
      const tbody = document.getElementById('tabelaSenioridade');
      
      if (!tbody) return;

      tbody.innerHTML = '';

      dados.forEach(item => {
        const idReal = item.idsenioridade !== undefined ? item.idsenioridade : (item.id || item.id_senioridade);
        console.log("ID detetado para exclusão:", idReal);

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${item.nivel}</td>
          <td>${item.descricao || 'Não informada'}</td>
          <td>
            <button class="btn btn-danger btn-sm" onclick="deletarSenioridade(${idReal})">Excluir</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (error) {
    console.error('Erro ao carregar senioridades:', error);
  }
}

async function deletarSenioridade(id) {
  if (!confirm(`Tens a certeza de que pretendes excluir esta senioridade (ID: ${id})?`)) {
    return;
  }

  const token = localStorage.getItem('token');

  try {
    const resposta = await fetch(`http://127.0.0.1:8000/senioridade/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (resposta.ok) {
      alert('Senioridade excluída com sucesso!');
      carregarSenioridades();
    } else {
      const erro = await resposta.json();
      alert('Erro ao excluir: ' + (erro.detail || erro.erro || 'Erro desconhecido'));
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    alert('Não foi possível conectar ao servidor.');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  carregarSenioridades();
});