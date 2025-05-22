# Proyecto-PUK
## 
Cosas a tener en cuenta. 

Escaneo de puertos

```bash
nmap -sS 172.18.0.0/16
```
utilizar el script start.sh para la inicialización de todo el proyecto.

Inicializar docker

```bash
docker compose up -d --build
```
Resetear Docker

```bash
docker compose up --build
docker image prune -a --force
```
.