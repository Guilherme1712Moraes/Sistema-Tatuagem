# ============================================================
# rotas/usuarios.py — Gestão e Registo de Utilizadores
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar
import bcrypt

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str = "funcional"

@router.post("/")
def criar_usuario(usuario: UsuarioSchema):
    conn = conectar()
    cursor = conn.cursor()

    # Encriptar a senha com bcrypt
    hashed_senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)",
            (usuario.nome, usuario.email, hashed_senha, usuario.tipo)
        )
        conn.commit()
        return {"mensagem": "Utilizador criado com sucesso!"}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        conn.close()