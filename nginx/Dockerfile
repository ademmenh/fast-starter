FROM nginx:1.29-alpine

RUN apk add --no-cache bash openssl

COPY templates/nginx.conf.template /etc/nginx/templates/default.conf.template

COPY start.sh /docker-entrypoint.d/

RUN chmod +x /docker-entrypoint.d/start.sh

RUN mkdir -p /var/www/tiles && chown -R nginx:nginx /var/www/tiles
