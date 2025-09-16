import json
import urllib
from urllib import request


#Gets the Current Patch from league of legends api.
def getPatch():
    with urllib.request.urlopen('http://ddragon.leagueoflegends.com/api/versions.json') as url:
        data = json.loads(url.read().decode())
        return data[0]