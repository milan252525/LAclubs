from flask import render_template, request, send_from_directory, make_response, redirect, url_for, jsonify, escape
from app import app, discord_oauth
import flask_discord
from . import get_data
import os
import re

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
    members = request.args.get('members', default = 95, type=int)

    lb_link = ""
    low = type is not None and type.lower() == "low"

    if type is None and country is None and region is None:
        type = "all"
        
    if type == "all":
        lb_link = "lb?limit=500"

    if type is not None:
        title = f"{type.upper()} CLUBS"
    elif region is not None:
        title = f"{region.upper()} CLUBS"
        lb_link = "region=" + region.lower()
    else:
        title = f"{country.upper()} CLUBS"
        lb_link = "country=" + country.lower()
        
    title = title.replace('EL', 'EL ').replace('REPUBLIC', ' REPUBLIC')

    clubs = get_data.get_clubs(region=region, country=country, type=type, members=members)
    
    resp = make_response(render_template('clubs.html', clubs=clubs, title=title, lb_link=lb_link, low=low))
    return resp

@app.route('/club')
def club():
    tag = request.args.get('tag', default= "")
    club = get_data.get_club(tag)
    if not club['success']:
        title='ERROR'
        history_link = ""
        log_link = ""
    else:
        title=club['name'].upper()
        history_link = "history/club?tag=" + tag.strip("#").upper()
        log_link = "history/log?tag=" + tag.strip("#").upper()
    resp = make_response(render_template('club_single.html', club=club, title=title, history_link=history_link, log_link=log_link))
    return resp

@app.route('/lb')
def lb():
    region = request.args.get('region', default= None)
    country = request.args.get('country', default= None)
    
    limit = request.args.get('limit', default = -1, type=int)
    url = f"/api/lb?limit={limit}"

    title = f"LA LEADERBOARD"
    if region is not None:
        region = escape(region)
        url = f"/api/lb?region={region.lower()}&limit={limit}" 
        title = f"{region.upper()} LEADERBOARD"
    elif country is not None:
        country = escape(country)
        url = f"/api/lb?country={country.lower()}&limit={limit}" 
        title = f"{country.upper()} LEADERBOARD"

    title = title.replace('EL', 'EL ').replace('REPUBLIC', ' REPUBLIC')

    resp = make_response(render_template('lb.html', title=title, request_url=url, limit=limit))
    return resp

@app.route('/history/club')
def history_club():
    tag = request.args.get('tag', default = "")
    url = f"/api/history/club?tag={tag}"
    name = get_data.get_club_name(tag)
    resp = make_response(render_template("history.html", request_url=url, name=name.upper() if name != "" else "NOT FOUND"))
    return resp

@app.route('/history/log')
def history_log():
    tag = request.args.get('tag', default = "")
    url = f"/api/history/log?tag={tag}"
    name = get_data.get_club_name(tag)
    resp = make_response(render_template("club_log.html", request_url=url, name=name.upper() if name != "" else "NOT FOUND"))
    return resp

@app.route('/api/lb')
def api_lb():
    region = request.args.get('region', default = None)
    country = request.args.get('country', default = None)

    limit = request.args.get('limit', default = -1, type=int)

    players = get_data.get_all_players(region=region, country=country)
    if limit < 0:
        return jsonify(players)
    else:
        return jsonify(players[:limit])

@app.route('/api/history/player')
def api_history_player():
    tag = request.args.get('tag', default = None)
    if tag is None:
        return {"status" : "missing_tag"}
    tag = "#" + tag.upper().replace("O", "0")
    allowed = '#0289PYLQGRJCUV'
    for c in tag:
        if c not in allowed:
            return {"status" : "invalid"}
    return jsonify(get_data.get_player_history(tag))

@app.route('/api/history/club')
def api_history_club():
    tag = request.args.get('tag', default = None)
    if tag is None:
        return {"status" : "missing_tag"}
    tag = tag.upper().replace("O", "0")
    tag = tag.upper()
    allowed = '0289PYLQGRJCUV'
    for c in tag:
        if c not in allowed:
            return {"status" : "invalid"}
    return jsonify(get_data.get_club_history(tag))

@app.route('/api/history/log')
def api_history_log():
    tag = request.args.get('tag', default = None)
    if tag is None:
        return {"status" : "missing_tag"}
    tag = tag.upper().replace("O", "0")
    tag = tag.upper()
    allowed = '0289PYLQGRJCUV'
    for c in tag:
        if c not in allowed:
            return {"status" : "invalid"}
    return jsonify(get_data.get_club_log(tag))

@app.route('/api/club')
def api_club():
    tag = request.args.get('tag', default = None)
    if tag is None:
        return {"status" : "missing_tag"}
    club = get_data.get_club(tag)
    if not club['success']:
        return {"status" : "invalid"} 
    return jsonify(get_data.get_club(tag))

@app.route('/api/clubs')
def api_clubs():
    region = request.args.get('region', default = None)
    country = request.args.get('country', default = None)
    type = request.args.get('type', default = None)
    members = request.args.get('members', default = 95, type=int)

    if type is None and country is None and region is None:
        type = "all"
        
    data = get_data.get_clubs(region=region, country=country, type=type, members=members)
    return jsonify(data)
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def error_404(error):
    return render_template("error.html", title="Error 404", error="404 - Our goblins could not find this page."), 404

@app.errorhandler(500)
def error_500(error):
    return render_template("error.html", title="Error 500", error="500 - Something went terribly wrong. Sorry for the inconvenience."), 500

""" @app.after_request
def add_header(resp):
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp """

#@app.route('/bs')
#def bs():
#    url = request.args.get('url', default = "https://laclubs.net")
#    title = request.args.get('title', default = "")
#    return redirect(f"brawlstars://webview?page={url}&popup_title={title}", code=302)

@app.route("/login/")
def login():
    return discord_oauth.create_session(scope=["identify", "guilds"])

@app.route("/dashboard/")
@flask_discord.requires_authorization
def dashboard():
    allowed = [230947675837562880]
    user = discord_oauth.fetch_user()
    print(user, user.id)
    if user.id in allowed:
        return make_response(render_template('dashboard.html', title="Dashboard", user=user))
    else:
        return render_template("error.html", title="Error 401", error="401 - You are not allowed to access this page."), 401

@app.errorhandler(flask_discord.Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/callback/")
def callback():
    discord_oauth.callback()
    return redirect(url_for(".dashboard"))
