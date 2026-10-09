const API_URL = "http://127.0.0.1:8000/clientes";

document.addEventListener("DOMContentLoaded", carregarClientes);

// Listar Clientes
async function carregarClientes() {
    const res = await fetch(API_URL);
    const clientes = await res.json();
    
    const tabela = document.getElementById("tabela-clientes");
    tabela.innerHTML = "";

    clientes.forEach(c => {
        tabela.innerHTML += `
            <tr>
                <td>${c.idcliente}</td>
                <td>${c.nome}</td>
                <td>${c.cpf}</td>
                <td>${c.telefone || '-'}</td>
                <td>${c.cidade || '-'}/${c.uf || '-'}</td>
                <td>
                    <button class="btn-delete" onclick="deletarCliente(${c.idcliente})">Excluir</button>
                </td>
            </tr>
        `;
    });
}

// Cadastrar Cliente
document.getElementById("form-cliente").addEventListener("submit", async (e) => {
    e.preventDefault();

    const clienteData = {
        nome: document.getElementById("nome").value,
        cpf: document.getElementById("cpf").value,
        telefone: document.getElementById("telefone").value,
        datacadastro: document.getElementById("datacadastro").value || null,
        cidade: document.getElementById("cidade").value,
        uf: document.getElementById("uf").value
    };

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(clienteData)
    });

    document.getElementById("form-cliente").reset();
    carregarClientes();
});

// Deletar Cliente
async function deletarCliente(id) {
    if (confirm("Tem certeza que deseja excluir?")) {
        await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        carregarClientes();
    }
}