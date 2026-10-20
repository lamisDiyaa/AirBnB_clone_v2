#!/usr/bin/env bash
# Set up Nginx and the web_static deployment directories.

set +e

if ! command -v nginx >/dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

cat > /data/web_static/releases/test/index.html <<'HTML'
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
HTML

rm -f /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

chown -R ubuntu:ubuntu /data/

cat > /etc/nginx/conf.d/web_static.conf <<'NGINX'
server {
    listen 80;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}
NGINX

nginx -t
if [ $? -eq 0 ]; then
    systemctl restart nginx
fi

exit 0
