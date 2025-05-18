FROM nginx:latest
COPY default.conf /etc/nginx/conf.d/default.conf
COPY htpasswd/.htpasswd /etc/nginx/.htpasswd
COPY html/index.html /usr/share/nginx/html/index.html
