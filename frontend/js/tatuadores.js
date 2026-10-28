// ============================================================
// tatuadores.js
// ============================================================

const API = 'http://127.0.0.1:8000';

protegerPagina();


const formTatuador =
    document.getElementById('form-tatuador');

const botaoSubmit =
    document.getElementById('btn-submit-tatuador');


// ============================================================
// CARREGAR SENIORIDADES
// ============================================================

async function carregarSenioridades() {

    try {

        const resposta =
            await fetchAutenticado(
                `${API}/senioridade/`
            );


        if (!resposta.ok) {

            const erro = await resposta.json();

            throw new Error(
                erro.detail ||
                'Erro ao carregar senioridades.'
            );
        }


        const senioridades =
            await resposta.json();


        const select =
            document.getElementById(
                'idsenioridade'
            );


        select.innerHTML = `
            <option value="">
                Selecione a senioridade...
            </option>
        `;


        senioridades.forEach(s => {

            const option =
                document.createElement('option');


            option.value =
                s.idsenioridade;


            option.textContent =
                s.nivel ||
                s.nome ||
                `Senioridade ${s.idsenioridade}`;


            select.appendChild(option);

        });


    } catch (erro) {

        console.error(
            'Erro ao carregar senioridades:',
            erro
        );

    }

}


// ============================================================
// CARREGAR ESTILOS
// ============================================================

async function carregarEstilos() {

    try {

        const resposta =
            await fetchAutenticado(
                `${API}/estilos/`
            );


        if (!resposta.ok) {

            const erro = await resposta.json();

            throw new Error(
                erro.detail ||
                'Erro ao carregar estilos.'
            );
        }


        const estilos =
            await resposta.json();


        const div =
            document.getElementById(
                'lista-estilos-checkbox'
            );


        div.innerHTML = '';


        if (estilos.length === 0) {

            div.innerHTML =
                '<span class="text-muted">Nenhum estilo cadastrado.</span>';

            return;
        }


        estilos.forEach(estilo => {

            const item =
                document.createElement('div');


            item.className =
                'form-check';


            item.innerHTML = `

                <input
                    class="form-check-input estilo-checkbox"
                    type="checkbox"
                    value="${estilo.idestilo}"
                    id="estilo_${estilo.idestilo}"
                >

                <label
                    class="form-check-label"
                    for="estilo_${estilo.idestilo}"
                >
                    ${estilo.descricao}
                </label>

            `;


            div.appendChild(item);

        });


    } catch (erro) {

        console.error(
            'Erro ao carregar estilos:',
            erro
        );

    }

}


// ============================================================
// LISTAR TATUADORES
// ============================================================

async function listarTatuadores() {

    try {

        const resposta =
            await fetchAutenticado(
                `${API}/tatuadores`
            );


        if (!resposta.ok) {

            const erro =
                await resposta.json();

            throw new Error(
                erro.detail ||
                'Erro ao listar tatuadores.'
            );

        }


        const tatuadores =
            await resposta.json();


        const corpo =
            document.getElementById(
                'corpo-tabela'
            );


        corpo.innerHTML = '';


        tatuadores.forEach(t => {


            const estilos =
                Array.isArray(t.estilos)
                    ? t.estilos
                        .map(e => e.descricao)
                        .join(', ')
                    : '';


            const tr =
                document.createElement('tr');


            tr.innerHTML = `

                <td>
                    ${t.idtatuador}
                </td>

                <td>
                    ${t.nome}
                </td>

                <td>
                    ${formatarCPF(t.cpf)}
                </td>

                <td>
                    ${t.senioridade_nome || ''}
                </td>

                <td>
                    ${estilos || 'Nenhum'}
                </td>

                <td>

                    <button
                        type="button"
                        class="btn btn-warning btn-sm me-2 editar"
                    >
                        Editar
                    </button>

                    <button
                        type="button"
                        class="btn btn-danger btn-sm excluir"
                    >
                        Excluir
                    </button>

                </td>

            `;


            tr.querySelector('.editar')
                .addEventListener(
                    'click',
                    () => preencherEdicao(t)
                );


            tr.querySelector('.excluir')
                .addEventListener(
                    'click',
                    () => deletarTatuador(
                        t.idtatuador
                    )
                );


            corpo.appendChild(tr);

        });


    } catch (erro) {

        console.error(
            'Erro ao listar tatuadores:',
            erro
        );

    }

}


// ============================================================
// CADASTRAR / EDITAR
// ============================================================

formTatuador.addEventListener(
    'submit',
    async function (event) {

        event.preventDefault();


        const nome =
            document
                .getElementById('nome')
                .value
                .trim();


        const cpf =
            document
                .getElementById('cpf')
                .value
                .replace(/\D/g, '');


        const email =
            document
                .getElementById('email')
                .value
                .trim();


        const telefone =
            document
                .getElementById('telefone')
                .value
                .trim();


        const datacontratacao =
            document
                .getElementById(
                    'datacontratacao'
                )
                .value;


        const idSenioridade =
            document
                .getElementById(
                    'idsenioridade'
                )
                .value;


        // Validar CPF

        if (cpf.length !== 11) {

            alert(
                'Digite um CPF com 11 números.'
            );

            return;

        }


        if (!idSenioridade) {

            alert(
                'Selecione uma senioridade.'
            );

            return;

        }


        const estilos =
            Array
                .from(
                    document.querySelectorAll(
                        '.estilo-checkbox:checked'
                    )
                )
                .map(
                    checkbox =>
                        parseInt(
                            checkbox.value
                        )
                );


        const dados = {

            nome: nome,

            cpf: cpf,

            email:
                email || null,

            telefone:
                telefone || null,

            datacontratacao:
                datacontratacao || null,

            idsenioridade:
                parseInt(idSenioridade),

            estilos: estilos

        };


        const id =
            formTatuador.dataset.idTatuador;


        try {

            let resposta;


            // =================================================
            // EDITAR
            // =================================================

            if (id) {

                resposta =
                    await fetchAutenticado(
                        `${API}/tatuadores/${id}`,
                        {

                            method: 'PUT',

                            headers: {
                                'Content-Type':
                                    'application/json'
                            },

                            body:
                                JSON.stringify(
                                    dados
                                )

                        }
                    );

            }


            // =================================================
            // CADASTRAR
            // =================================================

            else {

                resposta =
                    await fetchAutenticado(
                        `${API}/tatuadores`,
                        {

                            method: 'POST',

                            headers: {
                                'Content-Type':
                                    'application/json'
                            },

                            body:
                                JSON.stringify(
                                    dados
                                )

                        }
                    );

            }


            const resultado =
                await resposta.json();


            if (!resposta.ok) {

                throw new Error(
                    resultado.detail ||
                    resultado.erro ||
                    'Erro ao salvar tatuador.'
                );

            }


            alert(
                resultado.mensagem ||
                'Operação realizada com sucesso!'
            );


            limparFormulario();


            await listarTatuadores();


        } catch (erro) {

            console.error(
                'Erro ao salvar tatuador:',
                erro
            );


            alert(
                'Erro ao salvar tatuador: ' +
                erro.message
            );

        }

    }
);


// ============================================================
// EDITAR
// ============================================================

function preencherEdicao(tatuador) {


    document
        .getElementById('nome')
        .value =
        tatuador.nome || '';


    document
        .getElementById('cpf')
        .value =
        formatarCPF(
            tatuador.cpf || ''
        );


    document
        .getElementById('email')
        .value =
        tatuador.email || '';


    document
        .getElementById('telefone')
        .value =
        tatuador.telefone || '';


    // MySQL normalmente devolve
    // YYYY-MM-DD ou uma representação de data.

    let data = '';

    if (tatuador.datacontratacao) {

        data =
            String(
                tatuador.datacontratacao
            ).substring(0, 10);

    }


    document
        .getElementById(
            'datacontratacao'
        )
        .value = data;


    document
        .getElementById(
            'idsenioridade'
        )
        .value =
        tatuador.idsenioridade;


    formTatuador.dataset.idTatuador =
        tatuador.idtatuador;


    const estilosAtuais =
        Array.isArray(tatuador.estilos)
            ? tatuador.estilos.map(
                e => Number(e.idestilo)
            )
            : [];


    document
        .querySelectorAll(
            '.estilo-checkbox'
        )
        .forEach(checkbox => {

            checkbox.checked =
                estilosAtuais.includes(
                    Number(
                        checkbox.value
                    )
                );

        });


    botaoSubmit.textContent =
        'Salvar alteração';


    botaoSubmit.classList.remove(
        'btn-primary'
    );


    botaoSubmit.classList.add(
        'btn-success'
    );


    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });

}


// ============================================================
// EXCLUIR
// ============================================================

async function deletarTatuador(id) {


    const confirmar =
        confirm(
            'Tem certeza que deseja excluir este tatuador?'
        );


    if (!confirmar) {
        return;
    }


    try {

        const resposta =
            await fetchAutenticado(
                `${API}/tatuadores/${id}`,
                {
                    method: 'DELETE'
                }
            );


        const resultado =
            await resposta.json();


        if (!resposta.ok) {

            throw new Error(
                resultado.detail ||
                resultado.erro ||
                'Erro ao excluir tatuador.'
            );

        }


        alert(
            resultado.mensagem ||
            'Tatuador excluído com sucesso!'
        );


        await listarTatuadores();


    } catch (erro) {

        console.error(
            'Erro ao excluir:',
            erro
        );


        alert(
            'Erro ao excluir tatuador: ' +
            erro.message
        );

    }

}


// ============================================================
// LIMPAR FORMULÁRIO
// ============================================================

function limparFormulario() {


    formTatuador.reset();


    delete formTatuador.dataset.idTatuador;


    document
        .querySelectorAll(
            '.estilo-checkbox'
        )
        .forEach(
            checkbox =>
                checkbox.checked = false
        );


    botaoSubmit.textContent =
        'Cadastrar';


    botaoSubmit.classList.remove(
        'btn-success'
    );


    botaoSubmit.classList.add(
        'btn-primary'
    );

}


// ============================================================
// FORMATAR CPF
// ============================================================

function formatarCPF(cpf) {


    const numeros =
        String(cpf || '')
            .replace(/\D/g, '');


    if (numeros.length !== 11) {
        return numeros;
    }


    return numeros.replace(
        /(\d{3})(\d{3})(\d{3})(\d{2})/,
        '$1.$2.$3-$4'
    );

}


// ============================================================
// MÁSCARA DO CPF
// ============================================================

document
    .getElementById('cpf')
    .addEventListener(
        'input',
        function () {

            let valor =
                this.value
                    .replace(/\D/g, '')
                    .substring(0, 11);


            valor =
                valor.replace(
                    /(\d{3})(\d)/,
                    '$1.$2'
                );


            valor =
                valor.replace(
                    /(\d{3})(\d)/,
                    '$1.$2'
                );


            valor =
                valor.replace(
                    /(\d{3})(\d{1,2})$/,
                    '$1-$2'
                );


            this.value = valor;

        }
    );


// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener(
    'DOMContentLoaded',
    async function () {

        await carregarSenioridades();

        await carregarEstilos();

        await listarTatuadores();

    }
);