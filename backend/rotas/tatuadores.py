# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import conectar

router = APIRouter()


# ============================================================
# MODELO
# ============================================================

class Tatuador(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    datacontratacao: Optional[date] = None
    idsenioridade: int
    estilos: list[int] = []


# ============================================================
# GET — LISTAR TATUADORES
# Rota final: GET /tatuadores
# ============================================================

@router.get("/tatuadores")
def listar_tatuadores():

    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                t.idtatuador,
                t.nometatuador AS nome,
                t.cpf,
                t.email,
                t.telefone,
                t.datacontratacao,
                t.idsenioridade,
                s.nome AS senioridade_nome
            FROM tatuador t
            JOIN senioridade s
                ON t.idsenioridade = s.idsenioridade
            ORDER BY t.idtatuador
        """)

        tatuadores = cursor.fetchall()

        for tatuador in tatuadores:

            cursor.execute("""
                SELECT
                    e.idestilo,
                    e.descricao
                FROM estilo e
                JOIN tatuador_estilo te
                    ON e.idestilo = te.idestilo
                WHERE te.idtatuador = %s
                ORDER BY e.descricao
            """, (tatuador["idtatuador"],))

            tatuador["estilos"] = cursor.fetchall()

        return tatuadores

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar tatuadores: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# POST — CADASTRAR TATUADOR
# Rota final: POST /tatuadores
# ============================================================

@router.post("/tatuadores")
def criar_tatuador(tatuador: Tatuador):

    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Limpar CPF
        cpf = (
            tatuador.cpf
            .replace(".", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if len(cpf) != 11 or not cpf.isdigit():
            raise HTTPException(
                status_code=400,
                detail="O CPF deve conter 11 números."
            )

        # Verificar CPF duplicado
        cursor.execute(
            """
            SELECT idtatuador
            FROM tatuador
            WHERE cpf = %s
            """,
            (cpf,)
        )

        if cursor.fetchone():

            raise HTTPException(
                status_code=400,
                detail="Já existe um tatuador cadastrado com este CPF."
            )

        # Verificar senioridade
        cursor.execute(
            """
            SELECT idsenioridade
            FROM senioridade
            WHERE idsenioridade = %s
            """,
            (tatuador.idsenioridade,)
        )

        if not cursor.fetchone():

            raise HTTPException(
                status_code=400,
                detail="A senioridade selecionada não existe."
            )

        # Cadastrar tatuador
        cursor.execute(
            """
            INSERT INTO tatuador
            (
                nometatuador,
                cpf,
                email,
                telefone,
                datacontratacao,
                idsenioridade
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                tatuador.nome,
                cpf,
                tatuador.email,
                tatuador.telefone,
                tatuador.datacontratacao,
                tatuador.idsenioridade
            )
        )

        idtatuador = cursor.lastrowid

        # Cadastrar estilos N:N
        for idestilo in tatuador.estilos:

            cursor.execute(
                """
                INSERT INTO tatuador_estilo
                (idtatuador, idestilo)
                VALUES (%s, %s)
                """,
                (
                    idtatuador,
                    idestilo
                )
            )

        conn.commit()

        return {
            "mensagem": "Tatuador cadastrado com sucesso!",
            "idtatuador": idtatuador
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
            detail=f"Erro ao cadastrar tatuador: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# PUT — ATUALIZAR TATUADOR
# Rota final: PUT /tatuadores/{id}
# ============================================================

@router.put("/tatuadores/{id}")
def atualizar_tatuador(id: int, tatuador: Tatuador):

    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cpf = (
            tatuador.cpf
            .replace(".", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if len(cpf) != 11 or not cpf.isdigit():

            raise HTTPException(
                status_code=400,
                detail="O CPF deve conter 11 números."
            )

        # Verificar se tatuador existe
        cursor.execute(
            """
            SELECT idtatuador
            FROM tatuador
            WHERE idtatuador = %s
            """,
            (id,)
        )

        if not cursor.fetchone():

            raise HTTPException(
                status_code=404,
                detail="Tatuador não encontrado."
            )

        # Verificar CPF usado por OUTRO tatuador
        cursor.execute(
            """
            SELECT idtatuador
            FROM tatuador
            WHERE cpf = %s
            AND idtatuador <> %s
            """,
            (
                cpf,
                id
            )
        )

        if cursor.fetchone():

            raise HTTPException(
                status_code=400,
                detail="Já existe outro tatuador cadastrado com este CPF."
            )

        # Atualizar tatuador
        cursor.execute(
            """
            UPDATE tatuador
            SET
                nometatuador = %s,
                cpf = %s,
                email = %s,
                telefone = %s,
                datacontratacao = %s,
                idsenioridade = %s
            WHERE idtatuador = %s
            """,
            (
                tatuador.nome,
                cpf,
                tatuador.email,
                tatuador.telefone,
                tatuador.datacontratacao,
                tatuador.idsenioridade,
                id
            )
        )

        # Apagar associações antigas
        cursor.execute(
            """
            DELETE FROM tatuador_estilo
            WHERE idtatuador = %s
            """,
            (id,)
        )

        # Inserir estilos novamente
        for idestilo in tatuador.estilos:

            cursor.execute(
                """
                INSERT INTO tatuador_estilo
                (idtatuador, idestilo)
                VALUES (%s, %s)
                """,
                (
                    id,
                    idestilo
                )
            )

        conn.commit()

        return {
            "mensagem": "Tatuador atualizado com sucesso!"
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
            detail=f"Erro ao atualizar tatuador: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()


# ============================================================
# DELETE — EXCLUIR TATUADOR
# Rota final: DELETE /tatuadores/{id}
# ============================================================

@router.delete("/tatuadores/{id}")
def deletar_tatuador(id: int):

    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Primeiro remove os estilos relacionados
        cursor.execute(
            """
            DELETE FROM tatuador_estilo
            WHERE idtatuador = %s
            """,
            (id,)
        )

        # Depois remove o tatuador
        cursor.execute(
            """
            DELETE FROM tatuador
            WHERE idtatuador = %s
            """,
            (id,)
        )

        linhas_afetadas = cursor.rowcount

        if linhas_afetadas == 0:

            conn.rollback()

            raise HTTPException(
                status_code=404,
                detail="Tatuador não encontrado."
            )

        conn.commit()

        return {
            "mensagem": "Tatuador excluído com sucesso!"
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
            detail=f"Erro ao excluir tatuador: {str(erro)}"
        )

    finally:

        if conn and conn.is_connected():
            conn.close()