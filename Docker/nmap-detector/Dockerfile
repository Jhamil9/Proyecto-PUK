# Imagen base con Python y libpcap para Scapy
FROM python:3.9-slim

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y libpcap0.8 && \
    rm -rf /var/lib/apt/lists/*

# Crea directorio para logs
RUN mkdir -p /logs

# Copia dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script
COPY ids_script.py .

# Comando de inicio
ENTRYPOINT ["python", "ids_script.py"]