from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

import logging

API = FastAPI()
TAREFAS = []
LOGGER = logging.getLogger('devops_tarefas')
LOGGER.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('devops_tarefas.log', encoding='utf-8')
formatter = logging.Formatter(fmt="%(name)s | %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s")

file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

LOGGER.addHandler(file_handler)
LOGGER.addHandler(stream_handler)

class Tarefa(BaseModel):
    id: int
    titulo: str
    data_criacao: datetime
    finalizado: bool = False

async def criar_tarefa(titulo: str):
    LOGGER.info("Usuário acessou /criar")

    id = len(TAREFAS)
    tarefa_nova = Tarefa(id=id, titulo=titulo, data_criacao=datetime.now(), finalizado=False)
    
    LOGGER.debug(f"Criando tarefa {tarefa_nova}")

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}

async def pagina_inicial():
    LOGGER.info("Usuário acessou /")
    return {"mensagem": "Funcionando!"}

async def listar_tarefas():
    LOGGER.info("Usuário acessou /tarefas")
    return TAREFAS

async def autor():
    LOGGER.info("Usuário acessou /autor")
    return {"mensagem": "Pedro Rocha Horchulhack"}

async def rota_inexistente():
    LOGGER.error("Rota não existe")
    return {"mensagem": "Rota não existe"}

API.add_api_route("/tarefas", listar_tarefas, methods=['GET'])
API.add_api_route("/criar", criar_tarefa, methods=['POST'])
API.add_api_route("/", pagina_inicial, methods=['GET'])
API.add_api_route("/autor", autor, methods=['GET'])