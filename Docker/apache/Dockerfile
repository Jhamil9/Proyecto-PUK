FROM ubuntu:24.04

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

# 2) Limpia cualquier CRS y clona OWASP CRS
RUN rm -rf /usr/share/modsecurity-crs /etc/modsecurity/crs \
 && git clone --depth 1 -b v4.14.0 \
      https://github.com/coreruleset/coreruleset.git \
      /etc/modsecurity/crs \
 && cp /etc/modsecurity/crs/crs-setup.conf.example /etc/modsecurity/crs/crs-setup.conf \
 && rm /etc/modsecurity/crs/crs-setup.conf.example

# Cambia SecRuleEngine a 'On' y copia el archivo final
RUN sed -i 's/^SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf-recommended 

# 3) Prepara ModSecurity (carga solo tu setup + reglas)
RUN printf '%s\n' \
    "Include /etc/modsecurity/crs/crs-setup.conf" \
    "IncludeOptional /etc/modsecurity/crs/rules/*.conf" \
  >> /etc/apache2/conf-available/security2.conf

# 4) Habilita módulos necesarios
RUN a2enmod security2 auth_basic authn_file \
 && a2enconf security2

# 5) Copia el .htpasswd (pre‑generado en htpasswd/.htpasswd)
RUN mkdir -p /etc/apache2/.htpasswd
COPY htpasswd/.htpasswd /etc/apache2/.htpasswd/.htpasswd

# 6) Copia tu VirtualHost con la auth “in‑line” y los logs
COPY conf/000-default.conf /etc/apache2/sites-available/000-default.conf

# 7) Desactiva cualquier sitio por defecto y activa el tuyo
RUN a2dissite 000-default || true \
 && a2ensite 000-default

# 8) Define ServerName para silenciar el warning
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# 9) Copia tu web estática
COPY www/ /var/www/html/

EXPOSE 80 443
CMD ["apachectl", "-D", "FOREGROUND"]