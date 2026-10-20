#!/usr/bin/env bash
# Set up Nginx and directories for web_static deployment.

set +e

if ! command -v nginx >/dev/null 2>&1; then
    sudo apt-get update -y
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/releases
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

sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

NGINX_DEFAULT="/etc/nginx/sites-available/default"

if [ -f "$NGINX_DEFAULT" ]; then
    if ! sudo grep -q 'alias /data/web_static/current/;' "$NGINX_DEFAULT"; then
        sudo cp "$NGINX_DEFAULT" "${NGINX_DEFAULT}.backup"

        sudo python3 - "$NGINX_DEFAULT" <<'PYTHON'
import sys

path = sys.argv[1]

with open(path, "r", encoding="utf-8") as file:
    content = file.read()

location = """
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
"""

position = content.rfind("}")
if position != -1:
    content = content[:position] + location + content[position:]

with open(path, "w", encoding="utf-8") as file:
    file.write(content)
PYTHON
    fi
fi

if sudo nginx -t; then
    sudo systemctl restart nginx
fi

exit 0
