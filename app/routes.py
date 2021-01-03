from flask import render_template, request, send_from_directory, make_response, redirect, url_for
from app import app, discord
from flask_discord import requires_authorization, Unauthorized
from . import get_data
import os

@app.route('/')
@app.route('/index')
def index():
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/clubs')
def clubs():
    region = request.args.get('region', default = None)
    country = request.args.get('country', default = None)
    type = request.args.get('type', default = None)

    if type is None and country is None and region is None:
        type = "all"

    if type is not None:
        title = f"{type.upper()} CLUBS"
    elif region is not None:
        title = f"{region.upper()} CLUBS"
    else:
        title = f"{country.upper()} CLUBS"
        
    title = title.replace('EL', 'EL ').replace('REPUBLIC', ' REPUBLIC')

    clubs = get_data.get_clubs(region=region, country=country, type=type)
    
    resp = make_response(render_template('clubs.html', clubs=clubs, title=title))
    return resp

@app.route('/club')
def club():
    tag = request.args.get('tag', default = None)
    club = get_data.get_club(tag)
    if not club['success']:
        title='ERROR'
    else:
        title=club['name']

    resp = make_response(render_template('club_single.html', club=club, title=title))
    return resp

@app.route('/lb')
def lb():
    players = get_data.get_all_players()
    try:
        limit = int(request.args.get('limit', default = -1))
    except ValueError:
        limit = -1
    if limit > 0:
        players = players[:limit]

    resp = make_response(render_template('lb.html', players=players))
    return resp

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.after_request
def add_header(resp):
    resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp

@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))