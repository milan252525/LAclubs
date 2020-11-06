sudo venv/bin/gunicorn -w 4 -b 0.0.0.0:443 --certfile cert.pem --keyfile key.pem --log-level debug --timeout 90 app:app &
sudo venv/bin/gunicorn -w 2 -b 0.0.0.0:80 --log-level debug --timeout 90 app:app &&
fg

