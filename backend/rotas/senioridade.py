# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar

router = APIRouter()

class Senioridade(BaseModel):
    nome: str

# GET /senioridade — lista todas as senioridades
@router.get("/senioridade")
def listar_senioridade():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade")
    senioridades = cursor.fetchall()
    conn.close()
    return senioridades

# POST /senioridade — cadastra nova senioridade
@router.post("/senioridade")
def criar_senioridade(senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senioridade (nome) VALUES (%s)", (senioridade.nome,))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade cadastrada com sucesso"}

# PUT /senioridade/{id} — atualiza senioridade
@router.put("/senioridade/{id}")
def atualizar_senioridade(id: int, senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE senioridade SET nome=%s WHERE idsenioridade=%s", (senioridade.nome, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade atualizada com sucesso"}

# DELETE /senioridade/{id} — deleta senioridade
@router.delete("/senioridade/{id}")
def deletar_senioridade(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM senioridade WHERE idsenioridade = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Senioridade deletada com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir esta senioridade."}