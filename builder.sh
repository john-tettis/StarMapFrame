#!/bin/sh
# Backup database
cp /backend/app/db.sqlite3 /tmp/

rm -rf /var/www/html/*
rm -rf /backend/*

# Build and setup frontend
cd frontend && npm run build && mv dist/* /var/www/html/
cd ../backend && cp -r invoice/ /var/www/html/

# Move flask app to /backend
cp -r * /backend/
rm /backend/app/assets/backgrounds/.gitkeep
rm /backend/app/assets/wallpapers/.gitkeep

# Build and run backend
cd /backend/
apt install python3.9 python3.9-dev python3.9-venv
python3.9 -m venv sandbox
. "$(pwd)/sandbox/bin/activate"
pip install -r requirements.txt

# Restore database
cp /tmp/db.sqlite3 /backend/app/

# Restart services
systemctl stop backend.service && systemctl start backend.service
echo "\n\n\tServer is running....\n"