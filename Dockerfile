FROM python:3.12-slim 

# Host -> contêiner
COPY app/ app/
COPY requirements.txt .

# Instalando dependências
RUN pip install -U -r requirements.txt

ENTRYPOINT ["fastapi", "run"]