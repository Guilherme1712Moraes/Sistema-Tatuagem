from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes, senioridade, tatuadores, agendamentos, estilos

app = FastAPI()

# Configuração de CORS obrigatória para o Frontend (porta 5500) falar com o Backend (porta 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(senioridade.router)
app.include_router(estilos.router)
app.include_router(tatuadores.router)
app.include_router(agendamentos.router)
from rotas import clientes, senioridade, tatuadores, agendamentos, estilos, usuarios 

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])