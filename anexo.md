# Docker-compose

```
services:
# Adaptar al apache 
  webserver:
    build: ./apache
    container_name: apache-secure
    volumes:
      - ./logs/apache/error.log:/var/log/apache2/error.log
      - ./logs/apache/access.log:/var/log/apache2/access.log 
    networks:
      - proyecto_monitoring_net
    ports:
      - "8080:80"
    dns:
      - 8.8.8.8
```

```
# Fail2ban Servicio 
  fail2ban:
    build: ./fail2ban
    container_name: fail2ban
    volumes:
      - ./logs/apache/access.log:/var/log/apache2/access.log:ro
      - ./fail2ban/jail.local:/etc/fail2ban/jail.local:ro
      - ./fail2ban/filter.d:/etc/fail2ban/filter.d:ro
      - ./logs/fail2ban/fail2ban.log:/var/log/fail2ban.log 
    networks:
      - proyecto_monitoring_net
    cap_add:
      - NET_ADMIN
      - NET_RAW
    privileged: true
```

```
# Port Scanner
  port-scan-detector:
    build:
      context: ./nmap-detector
      dockerfile: Dockerfile
    container_name: nmap-detector
    networks:
      - proyecto_monitoring_net
    cap_add:
      - NET_RAW
      - NET_ADMIN
    volumes:
      - ./logs/scan:/logs
    environment:
      - THRESHOLD=15
      - TIME_WINDOW=60
```
```
# Elk

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.28
    container_name: elastic
    environment:
      - discovery.type=single-node
    ports:
      - 9200:9200
      - 9300:9300
    networks:
      - proyecto_monitoring_net

  logstash:
    build: ./elk/logstash
    container_name: logstash
    volumes:
      - ./elk/logstash/eventos.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    environment:
      - ELASTICSEARCH_HOST=elasticsearch
      - "LOGSTASH_PIPELINE_PATH=/usr/share/logstash/pipeline/logstash.conf"
    depends_on:
      - elasticsearch
    ports:
      - "5044:5044"
    networks:
      - proyecto_monitoring_net
```
```
  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.28
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - SERVER_PUBLICBASEURL=http://localhost:5601
    ports:
      - 5601:5601
    networks:
      - proyecto_monitoring_net
```
```
  filebeat:
    image: docker.elastic.co/beats/filebeat:8.10.3
    container_name: filebeat
    volumes:
      - ./logs:/logs
      - ./elk/filebeat/config/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    depends_on:
      - logstash
    networks:
      - proyecto_monitoring_net

```
```
networks:
  proyecto_monitoring_net:
    driver: bridge
```
# Servicios Dockerfile

## <a id="va1" href="https://github.com/Jhamil9/Proyecto-PUK/tree/e09914822d33f31c20c951bd1c2ee2b79de4f1ad/Docker/apache">Apache</a>

```
FROM ubuntu:24.04

# Usuraio y contraseña de acceso al servicio
ARG HTPASSWD_USER=admin
ARG HTPASSWD_PASS=admin


# 1) Instalación de Apache, ModSecurity, utils y apache2-utils
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      apache2 \
      libapache2-mod-security2 \
      apache2-utils \
      git \
      wget \
      ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# 2) Limpia cualquier archivo de CRS y clona OWASP CRS oficial
RUN rm -rf /usr/share/modsecurity-crs /etc/modsecurity/crs \
 && git clone --depth 1 -b v4.14.0 \
      https://github.com/coreruleset/coreruleset.git \
      /etc/modsecurity/crs \
 && cp /etc/modsecurity/crs/crs-setup.conf.example /etc/modsecurity/crs/crs-setup.conf \
 && rm /etc/modsecurity/crs/crs-setup.conf.example

# 3) Cambiar SecRuleEngine a 'On' y copia el archivo final
RUN sed -i 's/^SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf-recommended 

# 4) Prepara ModSecurity (cargar solo el setup + reglas)
RUN printf '%s\n' \
    "Include /etc/modsecurity/crs/crs-setup.conf" \
    "IncludeOptional /etc/modsecurity/crs/rules/*.conf" \
  >> /etc/apache2/conf-available/security2.conf

# 5) Habilitar los módulos necesarios
RUN a2enmod security2 auth_basic authn_file \
 && a2enconf security2

# 6) Copiar el .htpasswd (pre‑generado en htpasswd/.htpasswd)
RUN mkdir -p /etc/apache2/.htpasswd
COPY htpasswd/.htpasswd /etc/apache2/.htpasswd/.htpasswd

# 7) Copiar nuestro VirtualHost con la auth “in‑line” y los logs
COPY conf/000-default.conf /etc/apache2/sites-available/000-default.conf

# 8) Desactiva cualquier sitio por defecto y activa el que hemos copiado
RUN a2dissite 000-default || true \
 && a2ensite 000-default

# 9) Definir un ServerName para silenciar un posible warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# 10) Copia nuestra web estática
COPY www/ /var/www/html/

# 11 Abrir los puertos
EXPOSE 80 443
CMD ["apachectl", "-D", "FOREGROUND"]
```

## <a id="va1" href="https://github.com/Jhamil9/Proyecto-PUK/tree/e09914822d33f31c20c951bd1c2ee2b79de4f1ad/Docker/fail2ban">Fail2Ban</a>

```
FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y fail2ban iproute2 && \
    mkdir -p /etc/fail2ban/filter.d
CMD ["fail2ban-server", "-f", "-x"]
```

## <a id="va1" href="https://github.com/Jhamil9/Proyecto-PUK/tree/e09914822d33f31c20c951bd1c2ee2b79de4f1ad/Docker/nmap-detector">IDS</a>

```
FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y libpcap0.8 && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /logs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ids_script.py .
ENTRYPOINT ["python", "ids_script.py"]
```

## <a id="va1" href="https://github.com/Jhamil9/Proyecto-PUK/tree/e09914822d33f31c20c951bd1c2ee2b79de4f1ad/Docker/elk">ELK stack</a>

```
FROM docker.elastic.co/logstash/logstash:7.17.28

COPY eventos.conf /usr/share/logstash/pipeline/logstash.conf
```
