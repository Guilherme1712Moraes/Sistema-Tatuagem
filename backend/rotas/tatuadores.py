from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import conectar

router = APIRouter(prefix="/tatuadores", tags=["Tatuadores"])

class TatuadorSchema(BaseModel):
    nometatuador: str
    cpf: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    datacontratacao: Optional[str] = None
    idsenioridade: Optional[int] = 1

class TatuadorResponse(TatuadorSchema):
    idtatuador: int

# 1. Listar Tatuadores
@router.get("/", response_model=List[TatuadorResponse])
def listar_tatuadores():
    db = conectar()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tatuador")
        tatuadores = cursor.fetchall()
        return tatuadores
    finally:
        cursor.close()
        db.close()

# 2. Criar Tatuador
@router.post("/", response_model=TatuadorResponse)
def criar_tatuador(tatuador: TatuadorSchema):
    db = conectar()
    cursor = db.cursor()
    try:
        query = """
            INSERT INTO tatuador (nometatuador, cpf, email, telefone, datacontratacao, idsenioridade)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            tatuador.nometatuador,
            tatuador.cpf,
            tatuador.email,
            tatuador.telefone,
            tatuador.datacontratacao,
            tatuador.idsenioridade
        )
        cursor.execute(query, valores)
        db.commit()
        novo_id = cursor.lastrowid
        return {**tatuador.dict(), "idtatuador": novo_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

# 3. Deletar Tatuador
@router.delete("/{id}")
def deletar_tatuador(id: int):
    db = conectar()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM tatuador WHERE idtatuador = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tatuador não encontrado")
        return {"mensagem": "Tatuador removido com sucesso!"}
    finally:
        cursor.close()
        db.close()