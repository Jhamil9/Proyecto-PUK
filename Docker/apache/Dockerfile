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
