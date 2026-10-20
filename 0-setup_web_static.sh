#!/usr/bin/env bash

set +e

if ! command -v nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

sudo tee /data/web_static/releases/test/index.html > /dev/null <<'HTML'
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
HTML

sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

if [ -d /etc/nginx/sites-available ]; then
    sudo tee /etc/nginx/sites-available/web_static > /dev/null <<'NGINX'
server {
    listen 80;
    listen [::]:80;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}
NGINX

    sudo ln -sfn /etc/nginx/sites-available/web_static /etc/nginx/sites-enabled/web_static
fi

sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl restart nginx
fi

exit 0
