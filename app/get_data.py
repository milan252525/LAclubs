import json
import os
from time import time

def get_pres_vp_sen(members):
    pres = ""
    vp = 0
    sen = 0
    for m in members:
        if m['role'] == "president":
            pres = m['name']
        elif m['role'] == "vicePresident":
            vp += 1
        elif m['role'] == "senior":
            sen += 1
    return pres, vp, sen

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


def get_clubs(region, country, type):
    start = time()
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "club_data.json")
    with open(json_url) as f:
        all = json.load(f)

    result = []
    for club_tag in all:
        club = all[club_tag]
        pres, vp_count, sen_count = get_pres_vp_sen(club['members'])
        output = {
            'name': club['name'],
            'tag' : club_tag,
            'member_count': len(club['members']),
            'description': club['description'],
            'trophies': club['trophies'],
            'required_trophies': club['required'],
            'required_trophies_id': str(get_rank_id(club['required'])),
            'average': (int(club['trophies']/len(club['members'])) if len(club['members']) != 0 else 0),
            'president': pres,
            'badge': str(club['badge'] - 8000000),
            'type' : club['type'].lower(),
            'vp_count': vp_count,
            'sen_count': sen_count
        }
        if type == "all":
            result.append(output)
        elif type == "low" and len(club['members']) < 95:
            result.append(output)
        elif region is not None and club['region'].lower() == region.lower():
            result.append(output)
        elif country is not None and club['country'].lower() == country.lower():
            result.append(output)
    if type == "low":
        result.sort(key=lambda x: x['member_count'])
    else:
        result.sort(key=lambda x: x['trophies'], reverse=True)
    print("time to build clubs:", time() - start)
    return result

role_sort_values = {
    "president" : 0,
    "vicePresident" : 1,
    "senior" : 2,
    "member" : 3,
}

def get_club(tag):
    start = time()
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "club_data.json")
    with open(json_url) as f:
        all = json.load(f)

    club_tag = tag.upper().strip("#")

    try:
        club = all[club_tag]
    except KeyError:
        return {
            'success' : False,
            'badge': 'none'
        }

    output = {
        'success' : True,
        'name': club['name'],
        'tag' : club_tag,
        'badge': str(club['badge'] - 8000000),
        'members': club['members']
    }

    for member in output['members']:
        member['league_badge'] = str(get_rank_id(member['trophies']))
        member['role_sort'] = role_sort_values[member['role']]
        member['role'] = member['role'].replace('eP', 'e-P').title()

    print("time to build club:", time() - start)
    return output

def get_all_players():
    start = time()
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "club_data.json")
    with open(json_url) as f:
        all = json.load(f)

    result = []
    for club_tag in all:
        badge = str(all[club_tag]['badge'] - 8000000)
        club_name = all[club_tag]['name']
        for member in all[club_tag]['members']:
            output = {
                'name': member['name'],
                'tag': member['tag'],
                'trophies': member['trophies'],
                'club_name': club_name,
                'club_tag': club_tag,
                'league_badge': str(get_rank_id(member['trophies'])),
                'club_badge': badge,
                'icon': member['icon']['id']
            }
            result.append(output)
    
    result.sort(key=lambda x: x['trophies'], reverse=True)

    print("time to build lb:", time() - start)
    return result