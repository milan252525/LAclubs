from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

csp = {
    "default-src" : "'self'",
    'script-src': [ 
        "'self'",
        "www.google-analytics.com",
        "www.googletagmanager.com"
    ]
} 

Talisman(app, content_security_policy=csp,)

from app import routes
