# 1) Base: Ubuntu 24.04
FROM ubuntu:24.04

# 2) Instala Apache, ModSecurity, Git y utilidades
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      apache2 \
      libapache2-mod-security2 \
      git \
      wget \
      ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# 3) Habilita el módulo security2 (ModSecurity)
RUN a2enmod security2

# 4) Activa ModSecurity en modo “On” con acceso a cuerpo de petición
RUN mv /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf \
 && sed -ri \
      -e 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' \
      -e 's/SecRequestBodyAccess Off/SecRequestBodyAccess On/' \
      /etc/modsecurity/modsecurity.conf

# 5) (¡AJUSTE!) Asegúrate de borrar cualquier clon previo, clona OWASP CRS y prepara las reglas
RUN rm -rf /etc/modsecurity/crs \
 && git clone --depth 1 \
      -b v4.14.0 \
      https://github.com/coreruleset/coreruleset.git \
      /etc/modsecurity/crs \
 && cp /etc/modsecurity/crs/crs-setup.conf.example \
       /etc/modsecurity/crs/crs-setup.conf

# 6) Incluye todas las reglas CRS en la configuración de Apache
RUN echo "\
# OWASP CRS include\n\
IncludeOptional /etc/modsecurity/crs/*.conf\n\
" >> /etc/apache2/conf-available/security2.conf

# 7) Copia tu sitio estático al DocumentRoot
COPY www/ /var/www/html/

# 8) Exponer puertos y arrancar Apache en primer plano
EXPOSE 80 443
CMD ["apachectl", "-D", "FOREGROUND"]