#!/bin/bash
set -e

for f in access.log error.log; do
    if [ -L "/var/log/nginx/$f" ]; then
        rm -f "/var/log/nginx/$f"
    fi
done

mkdir -p /etc/nginx/ssl

if [ ! -f /etc/nginx/ssl/nginx.crt ] || [ ! -f /etc/nginx/ssl/nginx.key ]; then
    openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/CN=localhost"
else
    echo "SSL certificates already exist at /etc/nginx/ssl. Skipping generation."
fi
