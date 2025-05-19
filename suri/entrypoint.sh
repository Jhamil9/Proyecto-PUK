#!/bin/bash

# Detecta la interfaz principal automáticamente
IFACE=$(ip route | awk '/default/ {print $5; exit}')

echo "[*] Detectando interfaz: $IFACE"

if [ -z "$IFACE" ]; then
  echo "[!] No se pudo detectar la interfaz de red. Abortando."
  exit 1
fi

echo "[*] Actualizando reglas de Suricata con suricata-update..."
suricata-update

echo "[*] Iniciando Suricata en la interfaz $IFACE..."
exec suricata -c /etc/suricata/suricata.yaml -i "$IFACE"

