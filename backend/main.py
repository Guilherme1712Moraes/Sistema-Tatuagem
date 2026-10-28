from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from seguranca import verificar_token, verificar_admin
from rotas import (
    login,
    usuarios,
    clientes,
    tatuadores,
    agendamentos,
    estilos,
    senioridade
)


# ============================================================
# CONFIGURAÇÃO DA API
# ============================================================

app = FastAPI(
    title="Estúdio de Tatuagem API",
    version="0.1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOGIN
# ============================================================

app.include_router(
    login.router,
    tags=["Login"]
)


# ============================================================
# USUÁRIOS
# ============================================================

app.include_router(
    usuarios.router,
    prefix="/usuarios",
    tags=["Usuários"],
    dependencies=[Depends(verificar_admin)]
)


# ============================================================
# CLIENTES
# ============================================================

app.include_router(
    clientes.router,
    prefix="/clientes",
    tags=["Clientes"],
    dependencies=[Depends(verificar_token)]
)


# ============================================================
# SENIORIDADE
# ============================================================

# No senioridade.py as rotas são:
#
# @router.get("/")
# @router.post("/")
# @router.delete("/{id}")
#
# Portanto o prefixo deve ficar aqui.

app.include_router(
    senioridade.router,
    prefix="/senioridade",
    tags=["Senioridade"],
    dependencies=[Depends(verificar_token)]
)


# ============================================================
# ESTILOS
# ============================================================

app.include_router(
    estilos.router,
    prefix="/estilos",
    tags=["Estilos"],
    dependencies=[Depends(verificar_token)]
)


# ============================================================
# TATUADORES
# ============================================================

# IMPORTANTE:
#
# No tatuadores.py você já possui:
#
# @router.get("/tatuadores")
# @router.post("/tatuadores")
# @router.put("/tatuadores/{id}")
# @router.delete("/tatuadores/{id}")
#
# Por isso NÃO colocamos prefix="/tatuadores" aqui.
#
# Caso colocássemos, a rota ficaria:
#
# /tatuadores/tatuadores
#
# O que estaria errado para o seu frontend.

app.include_router(
    tatuadores.router,
    tags=["Tatuadores"],
    dependencies=[Depends(verificar_token)]
)


# ============================================================
# AGENDAMENTOS
# ============================================================

app.include_router(
    agendamentos.router,
    prefix="/agendamentos",
    tags=["Agendamentos"],
    dependencies=[Depends(verificar_token)]
)


# ============================================================
# ROTA PRINCIPAL
# ============================================================

@app.get("/")
def raiz():
    return {
        "mensagem": "API do Estúdio de Tatuagem a funcionar com segurança!"
    }