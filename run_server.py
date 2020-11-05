#!venv/bin/python

from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('139.59.139.93', 443), app, cert='key.pem')
http_server.serve_forever()
