FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y fail2ban iproute2 && \
    mkdir -p /etc/fail2ban/filter.d

CMD ["fail2ban-server", "-f", "-x"]
