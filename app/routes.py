from flask import render_template, request, send_from_directory, make_response, redirect, url_for, jsonify, escape
from flask_discord_interactions import Response, Embed, embed
from app import app, discord
#from flask_discord import requires_authorization, Unauthorized
from . import get_data
import os
import re
import enum

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
    tag = request.args.get('tag', default = None)
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
    region = request.args.get('region', default = None)
    country = request.args.get('country', default = None)
    
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

def clubs_to_embeds(clubs, title):
    embeds = []
    chunks = 20
    for i in range(0, len(clubs), chunks):
        fields = []
        chunk = clubs[i:i+chunks]
        for club in chunk:
            fields.append(
                embed.Field(
                    name=f"{club['name']} #{club['tag']}",
                    value=f"<:bstrophy:552558722770141204>`{club['trophies']}` <:people:449645181826760734>`{club['member_count']}/100`"
                )
            )
        embeds.append(
            Embed(
                title=title,
                fields=fields
            )
        )
    return embeds

regs = {
    "Asia": "AS",
    "Australia": "AU",
    "Europe": "EU",
    "Middle East": "ME",
    "North America": "NA",
    "Latin America": "LATAM"
}
Regions = enum.Enum("Regions", regs)
regs_reverse = dict()
for key, value in regs.items():
    regs_reverse[value] = key
    
@discord.command(annotations={"region": "Choose region"})
def region(ctx, region: Regions):
    "Clubs from region"
    clubs = get_data.get_clubs(region=region, country=None, type=None, members=None)
    embeds = clubs_to_embeds(clubs, f"LA - {regs_reverse[region]} clubs")
    return Response(embeds=embeds)


countries = {
    "United Kingdom": "UK",
    "Spain": "SPAIN",
    "Portugal": "PORTUGAL",
    "Poland": "POLAND",
    "Finland": "FINLAND",
    "Croatia": "CROATIA",
    "Singapore": "SINGAPORE",
    "India": "INDIA",
    "Bangladesh": "BANGLADESH",
    "USA": "USA",
    "Canada": "CANADA",
    "Hong Kong": "HONGKONG",
    "Argentina": "ARGENTINA",
    "Bolivia": "BOLIVIA",
    "Brazil": "BRAZIL",
    "Chile": "CHILE",
    "Dominican Republic": "DOMINICANREPUBLIC",
    "Guatemala": "GUATEMALA",
    "Mexico": "MEXICO",
    "Peru": "PERU",
    "Uruguay": "URUGUAY",
    "Venezuela": "VENEZUELA"
}
Countries = enum.Enum("Countries", countries)
countries_reverse = dict()
for key, value in countries.items():
    countries_reverse[value] = key

@discord.command(annotations={"country": "Choose country"})
def country(ctx, country: Countries):
    "Clubs from region"
    clubs = get_data.get_clubs(region=None, country=country, type=None, members=None)
    embeds = clubs_to_embeds(clubs, f"LA - {countries_reverse[country]} clubs")
    return Response(embeds=embeds)

@discord.command()
def low(ctx):
    "Clubs with low member count"
    clubs = get_data.get_clubs(region=None, country=None, type="low", members=95)
    embeds = clubs_to_embeds(clubs, f"LA - Low clubs")
    return Response(embeds=embeds)

#@app.route('/bs')
#def bs():
#    url = request.args.get('url', default = "https://laclubs.net")
#    title = request.args.get('title', default = "")
#    return redirect(f"brawlstars://webview?page={url}&popup_title={title}", code=302)
