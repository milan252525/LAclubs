from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('', 443), app, cert='key.pem')
http_server.serve_forever()