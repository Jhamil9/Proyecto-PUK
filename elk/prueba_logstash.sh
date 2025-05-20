#!/bin/bash

echo "🔄 Reiniciando servicios..."
docker compose down
docker compose up -d

echo "⏳ Esperando a que Logstash y Elasticsearch se inicien..."
sleep 10

echo -e "\n📤 Enviando eventos de prueba..."
for i in {1..5}; do
  echo "{\"message\":\"Evento de prueba $i desde $(hostname)\", \"timestamp\":\"$(date +'%Y-%m-%dT%H:%M:%S')\"}" | nc localhost 5044
done

echo -e "\n📋 Mostrando logs de Logstash..."
docker logs logstash | tail -n 20

echo -e "\n🔍 Comprobando índices en Elasticsearch..."
curl -s http://localhost:9200/_cat/indices?v

echo -e "\n🔎 Buscando eventos en Elasticsearch..."
INDEX_NAME="eventos-$(date +%Y.%m.%d)"
curl -s http://localhost:9200/${INDEX_NAME}/_search?pretty