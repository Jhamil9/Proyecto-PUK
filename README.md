<center>

# Implementación Segura de Docker en Ciberseguridad.
```
+---------------------+
|    Cliente Web      |
| (Acceso a Apache)   |
+----------+----------+
           |
           | HTTP/HTTPS
           v
+---------------------+     +----------------------+
|     Apache          |     |    OWASP CRS Rules   |
| (ModSecurity + WAF) +---->+ (Reglas de detección)|
+----------+----------+     +-----------+----------+
           |                            |
           | Logs de acceso/error       |
           v                            |
+---------------------+     +-----------v----------+
|    Fail2Ban         |     |   Puerto 5044        |
| (Bloqueo de IPs)    +<----+   Logstash           |
+----------+----------+     | (Procesamiento logs) |
           |              ^ +----------------------+
           |              |
           v              |
+---------------------+   |
| Detector de Escaneos|   |
| (Scapy + Python)    +---+
+----------+----------+
           |
           v
+---------------------+
|      ELK Stack      |
| (Elasticsearch,     |
|  Kibana, Filebeat)  |
+---------------------+
```
#### *Curso:* Ciberseguridad en Entornos de las Tecnologías de la Información.
</center>

- #### Cristian Manuel Hernández Cruellas	
- #### José Gael Hernández García	
- #### Jhamil Jesús Vargas Mariaca	
- #### Xabier Vega Castellà

---

## ÍNDICE

+ [Introducción](#id1)
+ [Justificación](#id2)
+ [Implementación](#id3)
+ [Posibles Mejoras Futuras](#id4)
+ [Conclusiones](#id5)
+ [Anexos](#id6)


+ [Bibliografía](#id7)

## *Introducción*. <a name="id1"></a>
Docker es una tecnología contenedor de aplicaciones construida sobre LXC que permite crear "contenedores", estas son aplicaciones empaquetadas auto-suficientes, muy livianas, capaces de funcionar en prácticamente cualquier ambiente, ya que tiene su propio sistema de archivos, librerías, terminal, etc.

## *Justificación*. <a name="id2"></a>

El objetivo es diseñar y desplegar un entorno seguro y monitorizable que permita simular, detectar y mitigar amenazas de seguridad en sistemas informáticos. Para lograrlo se pretende proteger los servicios desplegados y proporcionar visibilidad sobre posibles incidentes de seguridad, facilitando la detección temprana y la respuesta ante ataques. De este modo, se contribuye a mejorar la postura de seguridad y la capacidad de reacción frente a potenciales riesgos en la infraestructura tecnológica analizada.

En este caso, se trabaja con Docker y se implementan los servicios de Apache, ELK Stack, Fail2Ban y un sniffer de red.

Esta solución se ha elegido porque integra varias tecnologías y herramientas de referencia en la industria de la ciberseguridad, cada una cumpliendo un rol específico:

- **Apache**: Simula un servicio real expuesto a Internet.
```bash
├───apache
    │   └── Dockerfile
    ├───conf
    │     └── 000-default.conf
    ├───htpasswd
    │    └── .htpasswd
    └───www
         └── index.html
```


- **Fail2Ban**: Automatiza la detección y mitigación de ataques basados en patrones de logs y bloqueando IPs que realizan intentos como el acceso no autorizado alla web.

- NIDS personalizado: Es un sistema de detección de intrusiones en red desarrollado principalmente para identificar patrones de escaneo de puertos, como los que suelen generar herramientas de reconocimiento tipo Nmap.

- ELK Stack: Proporciona una plataforma centralizada para la recolección, almacenamiento, análisis y visualización de logs, permitiendo detectar patrones anómalos y responder a incidentes de manera informada.

## *Implementación*. <a name="id3"></a>

La principal herramienta que usamos es docker. Los servicios que se corren, depende de un sistema linux. Con la orquestacion de contenedores, `en este caso docker-compose.yml`, se logra configurar todos los servicios para que trabajen al unisono, permitiendo crear redes virtuales, volumenes persistentes como el caso de logs y algunas configuraciones comunes para que los contenedores puedan interactuar de manera segura y eficiente.

Cada servicio se construye a partir de su propio Dockerfile:

* Apache: El Dockerfile instala Apache, ModSecurity y OWASP CRS, configura autenticación básica y copia la configuración personalizada y los archivos web estáticos. Ademas expone el puerto 8080.

* Fail2Ban: El contenedor se construye sobre Ubuntu, instala Fail2Ban y copia las reglas y filtros personalizados, permitiendo, almacenar alertas de ataques y bloquear ip basadas en los logs.

* IDS personalizado: Utiliza una imagen con el servicio Python y la libreria Scapy que llama desde un archivo.txt para asi implementar un sniffer de red capaz de detectar escaneos de puertos en tiempo real, registrando alertas en un archivo de log compartido.

* ELK Stack:..... 

En la estructura del proyecto podemos ver que está organizado para facilitar la gestión y configuración de cada servicio de manera aislada y modular.

```
.
│   docker-compose.yml
│
├───apache
│   │   Dockerfile
│   ├───conf
│   │       000-default.conf
│   ├───htpasswd
│   │       .htpasswd
│   └───www
│           index.html
├───elk
│   │   prueba_logstash.sh
│   ├───elasticsearh
│   │       Dockerfile
│   │       jvm.options
│   ├───filebeat
│   │   └───config
│   │           filebeat.yml
│   └───logstash
│           Dockerfile
│           eventos.conf
├───fail2ban
│   │   Dockerfile
│   │   jail.local
│   └───filter.d
│           apache-auth.conf
├───logs
│   ├───apache
│   │       access.log
│   │       error.log
│   ├───fail2ban
│   │       fail2ban.log
│   └───scan
│           scan_sniffer.log
└───scan_sniffer
        Dockerfile
        scan_script.py
        requirements.txt

```
#### ¿Que conseguimos al configurarlo de esta manera?

Al configurar el entorno de esta manera, conseguimos un sistema eficiente y seguro, donde cada servicio opera de forma aislada en su propio contenedor, lo que minimiza riesgos y simplifica la gestión de dependencias. Además, se garantiza el poder desplegarse en cualquier máquina compatible con Docker.

## *Posibles Mejoras Futuras*. <a name="id4"></a>

### 🪶 Apache
Se podria implementar certificado SSL/TLS, Configurar reglas en Apache para forzar conexiones seguras con el protocolo HTTPS y deshabilitar protocolos y algoritmos obsoletos como TLS 1.0.

Tambien se podria usar la integración con LDAP/Active Directory para acceso restringido y Automatizar la actualización de .htpasswd mediante scripts o herramientas externas.

Cambiar puertos y desactivar servicios inecesarios

### 🚫 Fail2Ban
Usar fail2ban-server con persistencia en SQLite o PostgreSQL para mantener los bloqueos tras reinicios.
Tamien se pueden Integrar con listas negras de IPs maliciosas.
Crear filtros adicionales para detectar patrones únicos.

### 🐍 IDS
Detectar patrones de escaneo basados en distribución de puertos.
Ampliar análisis a otros tipos de paquetes para identificar escaneos pasivos.
Integrar con Fail2Ban o iptables para bloquear IPs automáticamente.
Registrar alertas en JSON para facilitar el procesamiento en ELK.

### 🌐 ELK stack
Definir un volumen (esdata) para preservar datos tras reinicios.
Habilitar seguridad en Elasticsearch/Kibana con usuarios y permisos para limitar accesos.
Cifrar comunicaciones entre Filebeat, Logstash y Elasticsearch.
Se podria implementar acciones de envío de alertas por email en jail.local
Añadir monitoreo de métricas del sistema como la CPU, memoria, red...

##  🐳 Mejoras generales Docker
Separar servicios en redes Docker distintas.
Configurar iptables o ufw en el host para restringir accesos no autorizados.
Usar herramientas como Watchtower para actualizar contenedores automáticamente.
Ejecutar periódicamente nuclei, bandit o kube-bench para detectar debilidades.
Configurar checks de salud en Docker Compose para reiniciar servicios fallidos automáticamente.

## *Conclusiones*. <a name="id5"></a>

## *Anexos*. <a name="id6"></a>

## *Bibliografía*. <a name="id7"></a>

