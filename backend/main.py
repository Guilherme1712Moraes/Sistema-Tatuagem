from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes

app = FastAPI()

# Permitir requisições do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)

@app.get("/")
def inicio():
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}