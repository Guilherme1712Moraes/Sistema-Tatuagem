# ============================================================
# rotas/estilos.py — CRUD de Estilos
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import conectar


router = APIRouter()


# ============================================================
# MODELO
# ============================================================

class Estilo(BaseModel):
    descricao: str


# ============================================================
# GET — LISTAR TODOS OS ESTILOS
# Rota final: GET /estilos/
# ============================================================

@router.get("/")
def listar_estilos():

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT idestilo, descricao
            FROM estilo
            ORDER BY descricao
            """
        )

        estilos = cursor.fetchall()

        return estilos

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar estilos: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# GET — BUSCAR ESTILO PELO ID
# Rota final: GET /estilos/{id}
# ============================================================

@router.get("/{id}")
def buscar_estilo(id: int):

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT idestilo, descricao
            FROM estilo
            WHERE idestilo = %s
            """,
            (id,)
        )

        estilo = cursor.fetchone()

        if not estilo:

            raise HTTPException(
                status_code=404,
                detail="Estilo não encontrado."
            )

        return estilo

    except HTTPException:

        raise

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar estilo: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# POST — CADASTRAR ESTILO
# Rota final: POST /estilos/
# ============================================================

@router.post("/")
def criar_estilo(estilo: Estilo):

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO estilo (descricao)
            VALUES (%s)
            """,
            (estilo.descricao,)
        )

        conn.commit()

        return {
            "mensagem": "Estilo cadastrado com sucesso",
            "idestilo": cursor.lastrowid
        }

    except Exception as erro:

        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar estilo: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# PUT — ATUALIZAR ESTILO
# Rota final: PUT /estilos/{id}
# ============================================================

@router.put("/{id}")
def atualizar_estilo(
    id: int,
    estilo: Estilo
):

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE estilo
            SET descricao = %s
            WHERE idestilo = %s
            """,
            (
                estilo.descricao,
                id
            )
        )

        conn.commit()

        if cursor.rowcount == 0:

            raise HTTPException(
                status_code=404,
                detail="Estilo não encontrado."
            )

        return {
            "mensagem": "Estilo atualizado com sucesso"
        }

    except HTTPException:

        if conn:
            conn.rollback()

        raise

    except Exception as erro:

        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar estilo: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# DELETE — EXCLUIR ESTILO
# Rota final: DELETE /estilos/{id}
# ============================================================

@router.delete("/{id}")
def deletar_estilo(id: int):

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor()

        # ----------------------------------------------------
        # Primeiro remove a associação N:N com tatuadores
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM tatuador_estilo
            WHERE idestilo = %s
            """,
            (id,)
        )

        # ----------------------------------------------------
        # Depois exclui o estilo
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM estilo
            WHERE idestilo = %s
            """,
            (id,)
        )

        linhas_afetadas = cursor.rowcount

        conn.commit()

        if linhas_afetadas == 0:

            raise HTTPException(
                status_code=404,
                detail="Estilo não encontrado."
            )

        return {
            "mensagem": "Estilo excluído com sucesso"
        }

    except HTTPException:

        if conn:
            conn.rollback()

        raise

    except Exception as erro:

        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao excluir estilo: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()