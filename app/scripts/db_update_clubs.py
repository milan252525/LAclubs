import time
import brawlstats
import json
import sys
import pymongo

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImFhOTVkZjBjLTNiYmYtNDkzNC05MWFlLWMxYTFkZDA3ZjQ5OSIsImlhdCI6MTYwNDU3MDc3NSwic3ViIjoiZGV2ZWxvcGVyLzFiNTkzZmFlLWRlNWItZDUwOS0zODI5LTg3OTg3YzZjOWI0ZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTg1LjcxLjIzMi4xOTQiLCIxMzkuNTkuMTM5LjkzIl0sInR5cGUiOiJjbGllbnQifV19.cDQGLc2t0V6AGVAo0KOW6CbKXffb856grnZjRvuS2qoDeRUwEKMUO1bvSBt7ZMwUjKsKeWW-HanEfGNTFp5btA"

try:
    api = brawlstats.Client(token)
except brawlstats.errors.ServerError:
    print("api server down")
    sys.exit()

myclient = pymongo.MongoClient("MONGO/")
collection = myclient['laclubs']['clubs']

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

with open("../data/clubs_input.json", "r") as clubs_file:
    clubs = json.load(clubs_file)

for club in clubs:
    tag = club['tag']
    print(f"Updating {club['name']}")
    try:
        data = api.get_club(tag)
        data = data.raw_data
    except brawlstats.errors.RequestError as e:
        print(e)
        print("API OFFLINE STOPPING...")
        sys.exit()
    try:
        pres, vp_count, sen_count = get_pres_vp_sen(data['members'])
        club_data = {
            'name': data['name'],
            'tag': tag,
            'description': data['description'],
            'trophies': data['trophies'],
            'required_trophies': data['requiredTrophies'],
            'type': data['type'].lower(),
            'badge': data['badgeId'],
            'members': data['members'],
            'member_count' : len(data['members']),
            'region': club['region'],
            'country': club['country'],
            'average': (int(data['trophies']/len(data['members'])) if len(data['members']) != 0 else 0),
            'president': pres,
            'vp_count': vp_count,
            'sen_count': sen_count
        }
    except KeyError:
        print(f"{club['name']} {tag} KEY ERROR")
        continue

    collection.update_one(
        {'tag': tag},
        {'$set': club_data},
        upsert=True
    )

    time.sleep(0.3)