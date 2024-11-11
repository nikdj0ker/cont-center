#!/bin/bash

# apt
mv /etc/apt/sources.list /etc/apt/sources.list.orig
cp /app/sources.list /etc/apt/sources.list
apt-get update

# init и procps
apt-get -y install init procps

# nginx
apt-get -y install nginx

# service
cp /app/thoth.service /etc/systemd/system/
cp /app/thoth.socket /etc/systemd/system/
ln -s /etc/systemd/system/thoth.service /etc/systemd/system/multi-user.target.wants/thoth.service

# requirements
pip install --no-cache-dir -r /app/requirements/production.txt
pip install --no-cache-dir -r /app/requirements/requirements.txt

# очистка
apt-get clean all
rm -rf /app
