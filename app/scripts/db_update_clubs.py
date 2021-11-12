import time
import brawlstats
import sys
import pymongo

token="TOKEN "

try:
    api = brawlstats.Client(token)
except brawlstats.errors.ServerError:
    print("api server down")
    sys.exit()

myclient = pymongo.MongoClient("MONGO/")
db = myclient['laclubs']

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

clubs = db['tracked_clubs'].find()

time_data = time.gmtime(int(time.time()))
save_history = time_data.tm_hour % 4 == 0 and time_data.tm_min < 5

errors = 0

for club in clubs:
    tag = club['tag']
    print(f"Updating {club['name']} {club['tag']}")
    try:
        data = api.get_club(tag)
        data = data.raw_data
    except brawlstats.errors.RequestError as e:
        print("ERROR, club['name'], club['tag'], e)
        errors += 1
        if error >= 3:
            print("API OFFLINE STOPPING...")
            sys.exit()
    try:
        pres, vp_count, sen_count = get_pres_vp_sen(data['members'])
        club_data = {
            'name': data['name'],
            'tag': tag,
            'description': data.get('description', ""),
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
        history = {
            'time' : int(time.time()),
            'name': data['name'],
            'tag': tag,
            'description': data.get('description', ""),
            'trophies': data['trophies'],
            'members': data['members'],
            'member_count' : len(data['members']),
            'required': data['requiredTrophies'],
            'badge': data['badgeId'],
            'type': data['type'].lower()
        }
    except KeyError:
        print(f"{club['name']} {tag} KEY ERROR")
        continue

    db['clubs'].update_one(
        {'tag': tag},
        {'$set': club_data},
        upsert=True
    )

    if save_history:
        db['club_history'].insert_one(history)

    time.sleep(0.1)
