#!/bin/sh
rm -rf /var/www/html/*
rm -rf /backend/*

cd frontend && npm run build && mv dist/* /var/www/html/
cd ../backend && cp -r invoice/ /var/www/html/

cp -r * /backend/

pip3 install virtualenv && python3 -m virtualenv env
source "$(pwd)/env/bin/activate"
pip install -r requirements.txt

exec ./run.sh