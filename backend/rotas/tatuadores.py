# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores com N:N de Estilos
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar

router = APIRouter()

class Tatuador(BaseModel):
    nome: str
    idsenioridade: int
    estilos: list[int] = []  # Lista de IDs dos estilos selecionados

# GET /tatuadores — Lista todos os tatuadores com os respetivos estilos
@router.get("/tatuadores")
def listar_tatuadores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    
    # Mapeia nometatuador como 'nome' para o frontend ler corretamente
    cursor.execute("""
        SELECT t.idtatuador, t.nometatuador as nome, t.idsenioridade, s.nome as senioridade_nome 
        FROM tatuador t
        JOIN senioridade s ON t.idsenioridade = s.idsenioridade
    """)
    tatuadores = cursor.fetchall()

    for tat in tatuadores:
        cursor.execute("""
            SELECT e.idestilo, e.descricao 
            FROM estilo e
            JOIN tatuador_estilo te ON e.idestilo = te.idestilo
            WHERE te.idtatuador = %s
        """, (tat["idtatuador"],))
        tat["estilos"] = cursor.fetchall()

    conn.close()
    return tatuadores

# POST /tatuadores — Cadastra novo tatuador e associa os estilos
@router.post("/tatuadores")
def criar_tatuador(tatuador: Tatuador):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO tatuador (nometatuador, idsenioridade) VALUES (%s, %s)",
        (tatuador.nome, tatuador.idsenioridade)
    )
    idtatuador = cursor.lastrowid

    for id_estilo in tatuador.estilos:
        cursor.execute(
            "INSERT INTO tatuador_estilo (idtatuador, idestilo) VALUES (%s, %s)",
            (idtatuador, id_estilo)
        )

    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador cadastrado com sucesso", "idtatuador": idtatuador}

# PUT /tatuadores/{id} — Atualiza tatuador e seus estilos
@router.put("/tatuadores/{id}")
def atualizar_tatuador(id: int, tatuador: Tatuador):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tatuador SET nometatuador = %s, idsenioridade = %s WHERE idtatuador = %s",
        (tatuador.nome, tatuador.idsenioridade, id)
    )

    cursor.execute("DELETE FROM tatuador_estilo WHERE idtatuador = %s", (id,))

    for id_estilo in tatuador.estilos:
        cursor.execute(
            "INSERT INTO tatuador_estilo (idtatuador, idestilo) VALUES (%s, %s)",
            (id, id_estilo)
        )

    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador atualizado com sucesso"}

# DELETE /tatuadores/{id} — Deleta um tatuador
@router.delete("/tatuadores/{id}")
def deletar_tatuador(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tatuador_estilo WHERE idtatuador = %s", (id,))
        cursor.execute("DELETE FROM tatuador WHERE idtatuador = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Tatuador deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"erro": f"Não foi possível excluir o tatuador: {str(e)}"}