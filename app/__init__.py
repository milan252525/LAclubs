from flask import Flask
from flask_talisman import Talisman
from flask_pymongo import PyMongo
from flask_discord import DiscordOAuth2Session
from flask_discord_interactions import DiscordInteractions

app = Flask(__name__)

app.secret_key = b'DG\xe0.\xb5\xc9\xf8\\\xa1u>J\xf9z\x14\xed'

app.config["MONGO_URI"] = "MONGO/laclubs"
mongo = PyMongo(app)

discord = DiscordInteractions(app)
app.config["DISCORD_CLIENT_ID"] = 795325486242857000
app.config["DISCORD_PUBLIC_KEY"] = "KEY"
app.config["DISCORD_CLIENT_SECRET"] = "SECRET"

app.config["DISCORD_REDIRECT_URI"] = "https://www.laclubs.net/callback"
discord_oauth = DiscordOAuth2Session(app)

csp = {
    "default-src" : [
        "'self'",
        "cdnjs.cloudflare.com"
    ],
    'script-src': [ 
        "'self'",
        "cdnjs.cloudflare.com",
    ],
    'img-src' : [
        "'self'",
        "cdn.brawlify.com"
    ],
    'connect-src' : [
        "'self'"
    ]
} 

Talisman(app, content_security_policy=csp, content_security_policy_nonce_in=['script-src'])

from app import routes
#from app import interactions

#discord.set_route("/interactions")
#discord.update_slash_commands(guild_id=401883208511389716)
#discord.update_slash_commands()


