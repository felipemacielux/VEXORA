# Pega a imagem base do Python na versão mais leve, como instalar um sistema operacional minímo com o Python 3.12 instalado
FROM python:3.12-slim
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && rm -rf /var/lib/apt/lists/*
# Define que todo trabalho acontecerá na pasta /app dentro do container
WORKDIR /app 
# Instala o Poetry, dentro do container
RUN pip install --no-cache-dir poetry
#Copia os arquivos de configuração do Poetry para o container
COPY requirements.txt /app/
# Configura o Poetry para instalar as dependências globalmente e instala as dependências (não em ambiente virtual)
RUN pip install --no-cache-dir -r requirements.txt
 #Copia o restante do código para o container
COPY . /app
# Expoe a porta 8000 do container para localhost:8000 no host
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]