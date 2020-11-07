from flask import render_template, request, send_from_directory
from app import app
from . import get_clubs
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

    clubs = get_clubs.get_clubs(region=region, country=country, type=type)
    
    return render_template('clubs.html', clubs=clubs, title=title)

@app.route('/club')
def club():
    tag = request.args.get('tag', default = None)
    member = request.args.get('member', default = None)
    club = get_clubs.get_club(tag)
    return render_template('club_single.html', club=club, title=club['name'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
