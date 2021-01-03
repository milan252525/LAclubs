from flask import Flask
from flask_talisman import Talisman
from flask_pymongo import PyMongo
from flask_discord import DiscordOAuth2Session

app = Flask(__name__)

app.config["MONGO_URI"] = "MONGO/laclubs"
app.config["DISCORD_CLIENT_ID"] = 795325486242857000    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "SECRET"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.

discord = DiscordOAuth2Session(app)

mongo = PyMongo(app)

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
