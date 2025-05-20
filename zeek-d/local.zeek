@load policy/misc/scan

# Ajusta el umbral de sensibilidad si lo necesitas
redef scan::sensitive = T;        # Opcional: activa sensibilidad alta
redef scan::threshold = 100;      # N° de conexiones distintas para activar alerta

# Opcional: activa log detallado
redef scan::scan_log = T;

