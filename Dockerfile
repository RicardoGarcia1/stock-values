# =============================================================
# BUILDER para crear dependencias compatibles con Lambda
# =============================================================
FROM --platform=linux/arm64 amazonlinux:2023 AS builder

# Actualiza sistema e instala herramientas necesarias
RUN dnf update -y && \
    dnf install -y python3.12 python3.12-pip python3.12-devel gcc zip && \
    dnf clean all

# Crea el directorio de trabajo
WORKDIR /var/task

# Copia requirements
COPY requirements.txt .

# Instala dependencias exactamente como Lambda las necesita
RUN pip3.12 install --no-cache-dir -r requirements.txt -t .

# Copia tu aplicación FastAPI
COPY app ./app
COPY data ./data
# Empaqueta todo en un ZIP
RUN zip -r lambda.zip .
