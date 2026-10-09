from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes, tatuadores, agendamentos  # ← Removido 'senioridade'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(tatuadores.router)
app.include_router(agendamentos.router)