const API = "http://127.0.0.1:8000";

// Bloqueia a página se não tiver login ativo
protegerPagina();

document.getElementById("formCadastro").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const resposta = await fetchAutenticado(`${API}/usuarios/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nome, email, senha, tipo: "funcional" })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            alert("Funcionário criado com sucesso!");
            window.location.href = "dashboard.html";
        } else {
            alert("Erro: " + (dados.detail || dados.erro || "Não foi possível criar o utilizador"));
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro de conexão com o servidor.");
    }
});