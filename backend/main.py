from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 1. Importar o StaticFiles
from rotas import clientes, tatuadores, agendamentos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Servir a pasta uploads de forma pública
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(clientes.router)
app.include_router(tatuadores.router)
app.include_router(agendamentos.router)