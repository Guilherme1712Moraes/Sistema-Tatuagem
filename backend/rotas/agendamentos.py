# ============================================================
# rotas/agendamentos.py — CRUD de Agendamentos
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

# Modelo Pydantic para validação das requisições
class Agendamento(BaseModel):
    idcliente: int
    idtatuador: int
    dataagendamento: str
    horaagendamento: str
    descricaotatuagem: Optional[str] = None
    valortatuagem: Optional[float] = None
    status: Optional[str] = None

# 1. Cadastrar Agendamento (POST)
@router.post("/")
def criar_agendamento(agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
             agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem)
        )
        conn.commit()
        return {"mensagem": "Agendamento cadastrado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# 2. Listar Agendamentos (GET)
@router.get("/")
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT agendamento.*, cliente.nome AS cliente, tatuador.nometatuador AS tatuador
            FROM agendamento
            JOIN cliente  ON agendamento.idcliente  = cliente.idcliente
            JOIN tatuador ON agendamento.idtatuador = tatuador.idtatuador
        """)
        agendamentos = cursor.fetchall()

        # Converter colunas timedelta (hora) e date (data) em string
        for a in agendamentos:
            if a.get("horaagendamento") is not None:
                total_segundos = int(a["horaagendamento"].total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                a["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            if a.get("dataagendamento") is not None:
                a["dataagendamento"] = str(a["dataagendamento"])

        return agendamentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# 3. Buscar Agendamento por ID (GET)
@router.get("/{id}")
def buscar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM agendamento WHERE idagendamento = %s", (id,))
        agendamento = cursor.fetchone()
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

        if agendamento.get("horaagendamento") is not None:
            total_segundos = int(agendamento["horaagendamento"].total_seconds())
            horas, resto = divmod(total_segundos, 3600)
            minutos, segundos = divmod(resto, 60)
            agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        if agendamento.get("dataagendamento") is not None:
            agendamento["dataagendamento"] = str(agendamento["dataagendamento"])

        return agendamento
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# 4. Atualizar Agendamento (PUT)
@router.put("/{id}")
def atualizar_agendamento(id: int, agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE agendamento
               SET idcliente=%s, idtatuador=%s, dataagendamento=%s, horaagendamento=%s,
                   descricaotatuagem=%s, valortatuagem=%s, status=%s
               WHERE idagendamento=%s""",
            (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
             agendamento.horaagendamento, agendamento.descricaotatuagem,
             agendamento.valortatuagem, agendamento.status, id)
        )
        conn.commit()
        return {"mensagem": "Agendamento atualizado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# 5. Deletar Agendamento (DELETE)
@router.delete("/{id}")
def deletar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM agendamento WHERE idagendamento = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        return {"mensagem": "Agendamento deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()