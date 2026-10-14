# ============================================================
# main.py — Ponto de entrada da API do Estúdio de Tatuagem
# ============================================================

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from seguranca import verificar_token
from rotas import login, usuarios, clientes, tatuadores, agendamentos, estilos, senioridade

app = FastAPI(title="Estúdio de Tatuagem API", version="0.1.0")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas (Login e Usuários ficam livres, as outras exigem token)
app.include_router(login.router, tags=["Login"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verificar_token)])
app.include_router(senioridade.router, prefix="/senioridade", tags=["Senioridade"], dependencies=[Depends(verificar_token)])
app.include_router(estilos.router, prefix="/estilos", tags=["Estilos"], dependencies=[Depends(verificar_token)])
app.include_router(tatuadores.router, prefix="/tatuadores", tags=["Tatuadores"], dependencies=[Depends(verificar_token)])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"], dependencies=[Depends(verificar_token)])

@app.get("/")
def raiz():
    return {"mensagem": "API do Estúdio de Tatuagem a funcionar com segurança!"}