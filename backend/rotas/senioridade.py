# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter()


class Senioridade(BaseModel):
    nivel: str
    descricao: Optional[str] = None


# ============================================================
# GET — LISTAR SENIORIDADES
# ============================================================

@router.get("/")
def listar_senioridade():
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM senioridade")
        senioridades = cursor.fetchall()

        resultado = []

        for s in senioridades:
            resultado.append({
                "idsenioridade": s["idsenioridade"],
                "nivel": s.get("nivel") or s.get("nome") or "Desconhecido",
                "descricao": s.get("descricao") or "Não informada"
            })

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar senioridades: {str(e)}"
        )

    finally:
        if conn and conn.is_connected():
            conn.close()


# ============================================================
# POST — CADASTRAR SENIORIDADE
# ============================================================

@router.post("/")
def criar_senioridade(item: Senioridade):
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Pelo seu tatuadores.py, a tabela senioridade usa
        # a coluna "nome".
        cursor.execute(
            """
            INSERT INTO senioridade (nome, descricao)
            VALUES (%s, %s)
            """,
            (item.nivel, item.descricao)
        )

        conn.commit()

        return {
            "mensagem": "Senioridade cadastrada com sucesso",
            "idsenioridade": cursor.lastrowid
        }

    except Exception as e:
        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar senioridade: {str(e)}"
        )

    finally:
        if conn and conn.is_connected():
            conn.close()


# ============================================================
# DELETE — EXCLUIR SENIORIDADE
# ============================================================

@router.delete("/{id}")
def deletar_senioridade(id: int):
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # ----------------------------------------------------
        # 1. Verifica se a senioridade existe
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT idsenioridade, nome
            FROM senioridade
            WHERE idsenioridade = %s
            """,
            (id,)
        )

        senioridade = cursor.fetchone()

        if not senioridade:
            raise HTTPException(
                status_code=404,
                detail=f"Senioridade com ID {id} não encontrada."
            )

        # ----------------------------------------------------
        # 2. Verifica se algum tatuador usa essa senioridade
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT idtatuador, nometatuador
            FROM tatuador
            WHERE idsenioridade = %s
            """,
            (id,)
        )

        tatuadores = cursor.fetchall()

        if tatuadores:
            nomes = ", ".join(
                tatuador["nometatuador"]
                for tatuador in tatuadores
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    "Não é possível excluir esta senioridade porque "
                    f"ela está sendo utilizada por: {nomes}. "
                    "Altere a senioridade desses tatuadores antes de excluí-la."
                )
            )

        # ----------------------------------------------------
        # 3. Se ninguém usa, pode excluir
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM senioridade
            WHERE idsenioridade = %s
            """,
            (id,)
        )

        conn.commit()

        return {
            "mensagem": "Senioridade excluída com sucesso!"
        }

    except HTTPException:
        if conn:
            conn.rollback()

        raise

    except Exception as e:
        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao excluir senioridade: {str(e)}"
        )

    finally:
        if conn and conn.is_connected():
            conn.close()