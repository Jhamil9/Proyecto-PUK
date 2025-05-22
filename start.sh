#!/bin/bash

# === COLORES PARA LA SALIDA ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# === FUNCIONES ===

function check_success {
  if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} $1 falló. Abortando."
    exit 1
  else
    echo -e "${GREEN}[OK]${NC} $1 completado."
  fi
}

function build_image {
  echo -e "${YELLOW}▶ Construyendo imagen: $1...${NC}"
  docker build --network host -t $1 $2
  check_success "Construcción de $1"
}

# === CONSTRUCCIÓN DE IMÁGENES ===

build_image "proyecto-puk-webserver" "./apache"
build_image "proyecto-puk-fail2ban" "./fail2ban"
build_image "proyecto-puk-port-scan-detector" "./nmap-detector"

# === INICIALIZACIÓN DE LOS CONTENEDORES ===

echo -e "${YELLOW}▶ Iniciando contenedores con Docker Compose...${NC}"
docker compose up -d
check_success "Inicialización de contenedores"

# === LISTADO DE CONTENEDORES ACTIVOS ===
echo -e "${GREEN}✔ Todos los servicios han sido levantados exitosamente.${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
