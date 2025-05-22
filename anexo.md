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
