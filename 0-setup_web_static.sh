#!/usr/bin/env bash
# Set up Nginx and the web_static deployment directories.

if ! command -v nginx >/dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html><head></head><body>School</body></html>" > /data/web_static/releases/test/index.html
ln -sfn /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/

rm -f /etc/nginx/conf.d/web_static.conf
conf=/etc/nginx/sites-available/default
if ! grep -q "hbnb_static" "$conf"; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$conf"
fi

service nginx restart
exit 0
