import json
from scraper.asset_scraper import ddragon_utils
from database import asset_db
from urllib import request
import urllib

def createChampionList():
    # Get Current Patch
    patch = ddragon_utils.getPatch()
    # Get ddragon champion list
    with urllib.request.urlopen(
            'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)) as url:
        data = json.loads(url.read().decode())
    champList = [{
        'champion_id': '-1',
        'champion_name': 'No Champion Data'
    }]
    for championName, championInfo in data['data'].items():
        champList.append({
            'champion_id': championInfo['key'],
            'champion_name': championName,
            'champion_image': 'https://ddragon.canisback.com/img/champion/tiles/{}_0.jpg'.format(championName),
        })
    return champList
    