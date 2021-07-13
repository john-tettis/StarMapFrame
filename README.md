# Starmap

This will generate starmap as `svg` image for you. You can customize date, time or coordinate of the stars as your wish... It uses [starmap-svg](https://github.com/skeletor-git/starmap-svg) to generate below image! In fact this repo is a web interface for working with `starmap-svg`!

![Example Output](./example/test.svg)

## Backend

Run below commands:

```bash
virtualenv env
source env/bin/acitavte
pip install -r requirements.txt

cd backend
sudo chmod +x run.sh
./run.sh
```

## Frontend

```bash
cd frontend
npm i
npm run start
```
