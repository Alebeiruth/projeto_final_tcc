# Base da imagem com Python
FROM python:3.13-slim

# Informações doa autores (opcional)
LABEL maintainer="Alexandre Beiruth <alexandre.beiruth@pucpr.edu.br>"
LABEL description="Projeto:  Comparação de Modelos para Reconhecimento de Expressões Faciais: Análise de Desempenho, Eficiência Computacional e Cross-Dataset Drift"

# Evita prompts interativos durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências básicas e SQLite CLI
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório para o app
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala as dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define o comando padrão ao iniciar o container
CMD ["python", "main_svm.py"]