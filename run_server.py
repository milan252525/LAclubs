from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('', 443), app)
http_server.serve_forever()