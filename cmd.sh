sudo venv/bin/gunicorn -w 3 -b 0.0.0.0:443 --certfile cert.pem --keyfile key.pem --log-level debug --timeout 90 -k "gevent" app:app &
sudo venv/bin/gunicorn -w 1 -b 0.0.0.0:80 --log-level debug --timeout 90 app:app &&
fg

