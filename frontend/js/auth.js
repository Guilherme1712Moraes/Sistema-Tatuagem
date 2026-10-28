// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// ============================================================


// ============================================================
// VERIFICAR SE EXISTE TOKEN
// ============================================================

function protegerPagina() {

    const token = localStorage.getItem('token');

    if (!token) {

        console.warn(
            'Nenhum token encontrado. Redirecionando para login...'
        );

        window.location.href = 'login.html';

        return false;
    }

    return true;
}


// ============================================================
// FETCH AUTENTICADO
// ============================================================

async function fetchAutenticado(url, opcoes = {}) {

    const token = localStorage.getItem('token');

    // Se não houver token, volta para o login
    if (!token) {

        console.warn(
            'Token não encontrado.'
        );

        window.location.href = 'login.html';

        throw new Error('Usuário não autenticado.');
    }


    // ========================================================
    // CONFIGURAR HEADERS
    // ========================================================

    opcoes.headers = {
        ...(opcoes.headers || {}),
        'Authorization': `Bearer ${token}`
    };


    try {

        console.log(
            'Requisição autenticada:',
            url
        );


        const resposta = await fetch(
            url,
            opcoes
        );


        console.log(
            `Resposta ${resposta.status}:`,
            url
        );


        // ====================================================
        // TOKEN INVÁLIDO OU EXPIRADO
        // ====================================================

        if (resposta.status === 401) {

            console.warn(
                'Token inválido ou expirado.'
            );

            localStorage.removeItem('token');

            window.location.href =
                'login.html';

            throw new Error(
                'Sessão expirada. Faça login novamente.'
            );
        }


        // ====================================================
        // ACESSO NEGADO
        // ====================================================

        if (resposta.status === 403) {

            console.error(
                'Acesso negado para:',
                url
            );
        }


        return resposta;


    } catch (erro) {

        console.error(
            'Erro na requisição:',
            url,
            erro
        );

        throw erro;
    }
}


// ============================================================
// LOGOUT
// ============================================================

function sair() {

    localStorage.removeItem('token');

    window.location.href =
        'login.html';
}