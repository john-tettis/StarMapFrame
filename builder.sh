#!/bin/sh
rm -rf /var/www/html/*
rm -rf /backend/*

cd frontend && npm run build && mv dist/* /var/www/html/
cd ../backend && cp -r invoice/ /var/www/html/

cp -r * /backend/

cd /backend/
apt install python3.9 python3.9-dev python3.9-venv
python3.9 -m venv sandbox
. "$(pwd)/sandbox/bin/activate"
pip install -r requirements.txt

exec systemctl stop backend.service && systemctl start backend.service