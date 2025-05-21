# Proyecto-PUK

Cosas a tener en cuenta. 

Escaneo de puertos

nmap -sS 172.18.0.0/16

utilizar el script start.sh para la inicialización de todo el proyecto.

resetear todos los contenedores
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker prune -a --force
