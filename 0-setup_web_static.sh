#!/usr/bin/env bash
# Configure Nginx and prepare directories for web_static deployment.

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

NGINX_CONFIG="/etc/nginx/sites-available/default"

if [ -f "$NGINX_CONFIG" ] && ! grep -q 'alias /data/web_static/current/;' "$NGINX_CONFIG"; then
    sed -i '/server_name _;/a\
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }' "$NGINX_CONFIG"
fi

if nginx -t; then
    systemctl restart nginx
fi

exit 0
