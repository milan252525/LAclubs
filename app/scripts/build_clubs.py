import json
with open("clubs.json") as f:
    data = json.load(f)
    clubs = data["5245652"]["GUILD"]["401883208511389716"]["clubs"]
    output = []
    for club_key in clubs:
        c = {
            "name" : clubs[club_key]["name"],
            "tag" : clubs[club_key]["tag"].upper(),
            "region" : "REGION",
            "country" : "COUNTRY"
        }
        output.append(c)

    with open("clubs_input.json", "w") as x:
        json.dump(output, x, indent=4)