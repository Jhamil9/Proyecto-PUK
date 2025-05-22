import os
from scapy.all import sniff, TCP, IP
import time
import logging

# Configuración desde variables de entorno
THRESHOLD = int(os.getenv("THRESHOLD", "10"))     # Umbral de paquetes SYN permitidos por IP en la ventana de tiempo
TIME_WINDOW = int(os.getenv("TIME_WINDOW", "10")) # Ventana de tiempo (en segundos) para contar los paquetes SYN

# Configuración del logging
logging.basicConfig(
    filename="/logs/port_scan_detection.log",      # Archivo donde se guardarán los logs de alertas
    level=logging.INFO,                            # Nivel de log: solo INFO y superiores
    format="%(asctime)s - %(message)s"             # Formato del mensaje de log con timestamp
)

# Diccionario para rastrear los timestamps de paquetes SYN por IP origen
syn_packets = {}

def detect_port_scan(packet):
    # Verifica si el paquete tiene capa TCP y si la flag es SYN ("S")
    if packet.haslayer(TCP) and packet[TCP].flags == "S":  # Solo SYN
        src_ip = packet[IP].src              # Obtiene la IP origen del paquete
        current_time = time.time()           # Timestamp actual

        # Si la IP no está en el diccionario, la inicializa con una lista vacía
        if src_ip not in syn_packets:
            syn_packets[src_ip] = []

        # Añade el timestamp actual a la lista de SYNs de esa IP
        syn_packets[src_ip].append(current_time)
        # Elimina los timestamps que estén fuera de la ventana de tiempo
        syn_packets[src_ip] = [t for t in syn_packets[src_ip] if current_time - t <= TIME_WINDOW]

        # Si el número de SYNs supera el umbral, se detecta posible escaneo de puertos
        if len(syn_packets[src_ip]) > THRESHOLD:
            msg = f"[!] Escaneo detectado desde {src_ip} (SYN: {len(syn_packets[src_ip])})"
            print(msg)            # Muestra alerta en consola
            logging.info(msg)     # Registra alerta en el archivo de log
            syn_packets[src_ip] = []  # Reinicia la lista para evitar alertas repetidas

def start_sniffer():
    print(f"[*] Iniciando sniffer (Umbral: {THRESHOLD}, Ventana: {TIME_WINDOW}s)...")
    try:
        # Inicia el sniffer en la interfaz de loopback ("lo"), solo captura tráfico TCP
        sniff(iface="eth0", filter="tcp", prn=detect_port_scan, store=False)
    except KeyboardInterrupt:
        print("\n[+] Saliendo...")  # Mensaje al salir con Ctrl+C
        exit(0)

if __name__ == "__main__":
    start_sniffer()  # Solo ejecuta el sniffer si el script se ejecuta directamente