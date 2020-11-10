from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

csp = {
    "default-src" : "'self'",
    'script-src': [ 
        "'self'",
        "*.googleanalytics.com",
        "*.google-analytics.com",
        "www.googletagmanager.com",
        "*.googleapis.com"
    ],
    'img-src' : [
        "'self'",
        "www.google-analytics.com"
    ],
    'connect-src' : "*.google-analytics.com"
} 

Talisman(app, content_security_policy=csp)

from app import routes
