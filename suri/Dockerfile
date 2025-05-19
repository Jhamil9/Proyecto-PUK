FROM jasonish/suricata:7.0.10

COPY conf/suricata.yaml /etc/suricata/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN chmod 755 /usr/bin/suricata

ENTRYPOINT ["/entrypoint.sh"]

