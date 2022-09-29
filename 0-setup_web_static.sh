#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
sudo app-get update -y
sudo app-get install nginx -y
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "\
<html>
  <head>
  </head>
  <body>
    Best School
  </body>
</html>" > /data/web_static/realeses/test/index.html
sudo ln -sf /data/web_static/realeses/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
content="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "34i\ $content" /etc/nginx/sites-enabled/default
sudo service nginx reload
sudo service nginx restart
