import os
import json

def parse_log_line(line):
    line = line.strip()

    # 1. Separar timestamp y el resto
    parts = line.split(" - ", 1)
    if len(parts) < 2:
        return None
    timestamp, rest = parts

    # 2. Extraer tipo_alerta (todo entre [ y ])
    if not rest.startswith("[") or "]" not in rest:
        return None
    end_bracket = rest.find("]")
    tipo_alerta = rest[1:end_bracket]

    # 3. Contenido después de la alerta
    content = rest[end_bracket+1:].strip()

    # 4. Dividir contenido acción/IP vs. paquete/conteo
    paren_idx = content.rfind("(")
    if paren_idx == -1 or not content.endswith(")"):
        return None
    action_ip_part = content[:paren_idx].strip()
    packet_part    = content[paren_idx+1:-1].strip()

    # 5. Separar acción e IP
    if " desde " not in action_ip_part:
        return None
    accion, ip_origen = action_ip_part.rsplit(" desde ", 1)
    accion    = accion.strip()
    ip_origen = ip_origen.strip()

    # 6. Separar tipo de paquete y conteo
    if ":" not in packet_part:
        return None
    tipo_paquete, conteo = packet_part.split(":", 1)
    tipo_paquete = tipo_paquete.strip()
    conteo       = conteo.strip()

    return {
        "timestamp":    timestamp,
        "tipo_alerta":  tipo_alerta,
        "accion":       accion,
        "ip_origen":    ip_origen,
        "tipo_paquete": tipo_paquete,
        "conteo":       int(conteo)
    }

def process_log_files(log_dir="logs/scan"):
    if not os.path.exists(log_dir):
        raise FileNotFoundError(f"No existe la carpeta '{log_dir}'")

    for filename in sorted(os.listdir(log_dir)):
        if not filename.endswith(".log"):
            continue
        path = os.path.join(log_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                result = parse_log_line(line)
                if result:
                    # Emitir JSON por línea, listo para ELK
                    print(json.dumps(result, ensure_ascii=False))
                # en caso de no parsear, simplemente lo ignoramos

if __name__ == "__main__":
    process_log_files()
