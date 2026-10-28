from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from database import conectar

router = APIRouter()

class Cliente(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    datacadastro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

@router.get("/")
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

@router.get("/{id}")
def buscar_cliente(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    if not cliente:
        return {"erro": "Cliente não encontrado"}
    return cliente

@router.post("/")
def criar_cliente(cliente: Cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO cliente (nome, cpf, telefone, datacadastro, cidade, uf)
            VALUES (%s, %s, %s, %s, %s, %s)""",
        (cliente.nome, cliente.cpf, cliente.telefone,
         cliente.datacadastro, cliente.cidade, cliente.uf)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente cadastrado com sucesso"}

@router.put("/{id}")
def atualizar_cliente(id: int, cliente: Cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE cliente
           SET nome=%s, cpf=%s, telefone=%s, datacadastro=%s, cidade=%s, uf=%s
           WHERE idcliente=%s""",
        (cliente.nome, cliente.cpf, cliente.telefone,
         cliente.datacadastro, cliente.cidade, cliente.uf, id)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente atualizado com sucesso"}

@router.delete("/{id}")
def deletar_cliente(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"mensagem": "Cliente deletado com sucesso"}
    except mysql.connector.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Este cliente possui agendamentos e não pode ser excluído."
        )
    finally:
        conn.close()