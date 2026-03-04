from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from datetime import datetime

from prometheus_client import start_http_server, Summary

import requests
import logging

async def startup():
    start_http_server(8001)

API = FastAPI(on_startup=[startup])
REQUEST = Summary('request_latency_seconds', 'Latência (segundos)')
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


@REQUEST.time()
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
    return {"mensagem": "Matheus Joave Baldo"}

async def rota_inexistente():
    LOGGER.error("Rota não existe")
    return {"mensagem": "Rota não existe"}

async def metricas():
    return PlainTextResponse(requests.get("http://localhost:8001").text)

API.add_api_route("/tarefas", listar_tarefas, methods=['GET'])
API.add_api_route("/criar", criar_tarefa, methods=['POST'])
API.add_api_route("/", pagina_inicial, methods=['GET'])
API.add_api_route("/autor", autor, methods=['GET'])
API.add_api_route("/metricas", metricas, methods=['GET'])