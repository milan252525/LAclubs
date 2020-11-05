sudo venv/bin/gunicorn -w 4 -b 139.59.139.93:443 --certfile cert.pem --keyfile key.pem app:app

