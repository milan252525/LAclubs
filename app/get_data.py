import json
import os
from time import time
from app import mongo
import re

def get_rank_id(trophies):
    if trophies < 500:
        return 0
    elif trophies < 1000:
        return 1
    elif trophies < 2000:
        return 2
    elif trophies < 3000:
        return 3
    elif trophies < 4000:
        return 4
    elif trophies < 6000:
        return 5
    elif trophies < 8000:
        return 6
    elif trophies < 10000:
        return 7
    elif trophies < 16000:
        return 8
    elif trophies < 30000:
        return 9
    elif trophies < 50000:
        return 10
    else:
        return 11

def get_clubs(region, country, type, members):
    if type == "all":
        filter = {}
    elif type == "low":
        filter = {"member_count" : { "$lt": members }}
    elif region is not None:
        regex = re.compile('[^a-zA-Z]')
        region_safe = regex.sub('', region)
        filter = {"region" : region_safe.upper()}
    elif country is not None:
        regex = re.compile('[^a-zA-Z]')
        country_safe = regex.sub('', country)
        filter = {"country" : country_safe.upper()}
    else:
        filter = {}
    
    result = list(mongo.db.clubs.find(filter))

    for club in result:
        club['required_trophies_id'] = str(get_rank_id(club['required_trophies']))
        club['badge'] = str(club['badge'] - 8000000)

    if type == "low":
        result.sort(key=lambda x: x['member_count'])
    else:
        result.sort(key=lambda x: x['trophies'], reverse=True)
    return result
        

role_sort_values = {
    "president" : 0,
    "vicePresident" : 1,
    "senior" : 2,
    "member" : 3,
}

def get_club(tag):
    regex = re.compile('[^a-zA-Z0-9]')
    tag_safe = regex.sub('', tag.upper().strip("#"))
    club = mongo.db.clubs.find_one({"tag": tag_safe})

    if club is None:
        return {
            'success' : False,
            'badge': 'none'
        }

    club['success'] = True
    club['badge'] = str(club['badge'] - 8000000)
    for member in club['members']:
        member['league_badge'] = str(get_rank_id(member['trophies']))
        member['role_sort'] = role_sort_values[member['role']]
        member['role'] = member['role'].replace('eP', 'e-P').title()
    return club

def get_all_players(region, country):
    if region is not None:
        regex = re.compile('[^a-zA-Z]')
        region_safe = regex.sub('', region)
        filter = {"region" : region_safe.upper()}
    elif country is not None:
        regex = re.compile('[^a-zA-Z]')
        country_safe = regex.sub('', country)
        filter = {"country" : country_safe.upper()}
    else:
        filter = {}
    clubs = mongo.db.clubs.find(filter)
    result = []
    for club in clubs:
        badge = str(club['badge'] - 8000000)
        for member in club['members']:
            member['name'] = member['name'].replace("﷽", "_")
            member['club_name'] = club['name']
            member['club_tag'] = club['tag']
            member['league_badge'] = str(get_rank_id(member['trophies']))
            member['club_badge'] = badge
            member['icon'] = member['icon']['id']
            result.append(member)
    result.sort(key=lambda x: x['trophies'], reverse=True)
    return result

def get_player_history(tag):
    filter = {"members.tag": tag}
    limit_field = {"members.$":1,"time":1}
    history = mongo.db.club_history.find(filter, limit_field).sort("time", 1)
    times = []
    trophies = []
    for entry in history:
        times.append(entry["time"])
        trophies.append(entry["members"][0]["trophies"])
    return {"trophies" : trophies, "times" : times}

def get_club_history(tag):
    filter = {"tag": tag}
    limit_field = {"trophies":1,"time":1}
    history = mongo.db.club_history.find(filter, limit_field).sort("time", 1)
    times = []
    trophies = []
    for entry in history:
        times.append(entry["time"])
        trophies.append(entry["trophies"])
    return {"trophies" : trophies, "times" : times}