from app import app, discord
from flask_discord_interactions import Response, Embed, embed
from . import get_data
import enum

club_status = {
    "inviteonly" : {"name": "Invite Only", "emoji": "<:invite_only:729734736490266625>"},
    "closed" : {"name": "Closed", "emoji": "<:locked:729734736573890570>"},
    "open" : {"name": "Open", "emoji": "<:open:729734736695787564> "}
}

club_badges = {
    '0': '<:00:717767397812994140>', 
    '1': '<:01:717767397364465687>', 
    '2': '<:02:717767397494358088>', 
    '3': '<:03:717767397662261258>', 
    '4': '<:04:717767397620187207>', 
    '5': '<:05:717767397259346031>', 
    '6': '<:06:717767397590695936>', 
    '7': '<:07:717767397586501763>', 
    '8': '<:08:717767397611798528>', 
    '9': '<:09:717767397272059905>', 
    '10': '<:10:717767397615861911>', 
    '11': '<:11:717767397578113044>', 
    '12': '<:12:717767397485969438>', 
    '13': '<:13:717767397519523990>', 
    '14': '<:14:717767397519654963>', 
    '15': '<:15:717767397611798598>', 
    '16': '<:16:717767397435506689>', 
    '17': '<:17:717767397049630788>', 
    '18': '<:18:717767397175721985>', 
    '19': '<:19:717767397398020236>', 
    '20': '<:20:717767397486100570>', 
    '21': '<:21:717767397381242970>', 
    '22': '<:22:717767397427380256>', 
    '23': '<:23:717767397175590994>', 
    '24': '<:24:717767397360271461>', 
    '25': '<:25:717767397423186021>', 
    '26': '<:26:717767397016207422>', 
    '27': '<:27:717767396974264371>', 
    '28': '<:28:717767397267734658>', 
    '29': '<:29:717767397129584681>'
}

def get_league_emoji(trophies : int):
    if trophies < 500:
        return "<:league_icon_00:553294108802678787>"
    elif trophies < 1000:
        return "<:league_icon_01:553294108735569921>"
    elif trophies < 2000:
        return "<:league_icon_02:553294109167583296>"
    elif trophies < 3000:
        return "<:league_icon_03:553294109264052226>"
    elif trophies < 4000:
        return "<:league_icon_04:553294344413511682>"
    elif trophies < 6000:
        return "<:league_icon_05:553294344912764959>"
    elif trophies < 8000:
        return "<:league_icon_06:553294344841461775>"
    elif trophies < 10000:
        return "<:league_icon_07:553294109515972640>"
    elif trophies < 16000:
        return "<:league_icon_08:553294109217914910>"
    elif trophies < 30000:
        return "<:league_icon_09:729644184616828928>"
    elif trophies < 50000:
        return "<:league_icon_10:729644185199575140>"
    else:
        return "<:league_icon_11:729644185778520115>"

def clubs_to_embeds(clubs, title):
    embeds = []
    chunks = 10
    first = True
    for i in range(0, len(clubs), chunks):
        fields = []
        chunk = clubs[i:i+chunks]
        for club in chunk:
            status_em = club_status[club['type']]['emoji']
            req = club['required_trophies']
            req_em = get_league_emoji(club['required_trophies'])
            badge = club_badges[str(club['badge'])]
            fields.append(
                embed.Field(
                    name=f"{badge} {club['name']} #{club['tag']}",
                    value=f"{status_em} <:bstrophy:552558722770141204>`{club['trophies']}` {req_em}`{req}+` <:people:449645181826760734>`{club['member_count']}/100`"
                )
            )
        embeds.append(
            Embed(
                title=title if first else None,
                fields=fields,
                color=1428501
            )
        )
        first = False
    return embeds[:10]

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
    for e in embeds:
        ctx.send(Response(embed=e))
    return "done"#Response(embeds=embeds)

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