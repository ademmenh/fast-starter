FROM nginx:1.29-alpine

RUN apk add --no-cache bash openssl libcap

RUN setcap cap_net_bind_service=+ep /usr/sbin/nginx

COPY nginx.conf /etc/nginx/nginx.conf

COPY templates/nginx.conf.template /etc/nginx/templates/default.conf.template

COPY start.sh /docker-entrypoint.d/40-generate-certs.sh

RUN chmod +x /docker-entrypoint.d/40-generate-certs.sh

RUN rm -f /var/log/nginx/access.log /var/log/nginx/error.log && \
    mkdir -p /var/log/nginx /etc/nginx/ssl /var/cache/nginx && \
    chown -R nginx:nginx \
        /var/log/nginx \
        /etc/nginx/ssl \
        /var/cache/nginx \
        /etc/nginx/conf.d

USER nginx
